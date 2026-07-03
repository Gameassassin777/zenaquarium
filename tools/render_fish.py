#!/usr/bin/env python3
"""render_fish.py — render specific fish species in isolation for art QC.

Generates one screenshot per species at high resolution so each can be
individually critiqued by Gemini vision.

Usage:
  python3 render_fish.py                    # default: render ALL catchable species → /tmp/zen_fish
  python3 render_fish.py /out/dir           # render all catchable species → custom dir
  python3 render_fish.py /out/dir guppy betta  # render only specific species
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

GAME = os.path.expanduser("~/zenaquarium/index.html")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/zen_fish"
os.makedirs(OUT, exist_ok=True)

# If specific species requested after OUT, use those; otherwise render all
ALL_CATCHABLE = [
    "guppy", "tetra", "goldfish", "betta", "angelfish", "discus",
    "jellyfish", "octopus", "turtle", "whaleshark", "narwhal", "lionfish",
    "seahorse", "idol", "mantaray", "cuttlefish", "pufferfish", "dragoneel",
    "seadragon", "colossalsquid",
    "viperfish", "gulper", "anglerfish", "isopod", "vampiresquid",
    "oarfish", "megamouth", "frilledshark", "siphonophore", "leviathan",
]
SPECIES = sys.argv[2:] if len(sys.argv) > 2 else ALL_CATCHABLE

# JS template: spawn one fish of given type at center, lock camera, hide UI
def spawn_js(species):
    return f"""
(() => {{
  try {{
    fishList.length = 0;
    seaweeds.length = 0;       // clear foreground seagrass/kelp so it doesn't overlap the QC fish
    snails.length = 0;
    clams.length = 0;
    particles.length = 0;
    marineSnow.length = 0;
    spawnFish({repr(species)});
    const f = fishList[0];
    if (!f) return 'ERR: spawnFish returned no fish';
    f.x = W / 2;
    f.y = H / 2;
    f.vx = 0.4; f.vy = 0;
    f.age = 60000;
    f.scale = 5.0;          // zoom x5 so the fish fills the QC frame
    f.hunger = 100;
    f.bonded = 0;
    return 'OK';
  }} catch(e) {{ return 'ERR:' + e.message + ' // ' + (e.stack||''); }}
}})()
    """

CLOSE_MODALS = """
(() => {
  try { claimDaily && claimDaily(); } catch(e){}
  try { collectOffline && collectOffline(); } catch(e){}
  ['wmodal','dmodal','lvlmodal','era-modal'].forEach(id => {
    const m = document.getElementById(id); if (m) m.classList.remove('show');
  });
  document.querySelectorAll('.modal.show').forEach(m => m.classList.remove('show'));
})()
"""

UNLOCK = """
(() => {
  try {
    playerLevel = 50;
    playerXP = 100000000;
    coins = 100000000;
    if (typeof boughtCounts === 'object' && boughtCounts !== null) {
      for (const k in TYPES) if (typeof boughtCounts[k] === 'undefined') boughtCounts[k] = 0;
    }
    try { currentEra = 5; } catch(e){}
    try { checkLevel && checkLevel(); } catch(e){}
    try { updateHUD && updateHUD(); } catch(e){}
    return 'OK';
  } catch(e) { return 'ERR:' + e.message; }
})()
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for species in SPECIES:
            page = await browser.new_page(
                viewport={"width": 900, "height": 600},
                device_scale_factor=2,
                color_scheme="dark",
            )
            await page.goto(f"file://{GAME}")
            await page.wait_for_load_state("networkidle", timeout=15000)
            try:
                await page.evaluate(CLOSE_MODALS)
            except Exception:
                pass
            await page.wait_for_timeout(300)
            try:
                await page.evaluate(UNLOCK)
            except Exception:
                pass
            await page.wait_for_timeout(500)
            try:
                result = await page.evaluate(spawn_js(species))
                if isinstance(result, str) and result.startswith("ERR"):
                    print(f"  ! {species}: {result[:300]}")
            except Exception as e:
                print(f"  ! {species}: {str(e)[:200]}")
            # Let animation cycle play for ~2s so we capture a typical pose
            await page.wait_for_timeout(2000)
            # DIAGNOSTIC: check if seaweeds repopulated between spawn and screenshot
            try:
                pre_shot = await page.evaluate("JSON.stringify({sw:seaweeds.length, swCount:typeof spawnSeaweed, part:particles.length, ms:marineSnow.length, fl:fishList.length})")
                print(f"    [state] {pre_shot}")
            except Exception as e:
                print(f"    [state-err] {str(e)[:150]}")
            out = os.path.join(OUT, f"{species}.png")
            await page.screenshot(path=out)
            print(f"  → {out}")
            await page.close()
        await browser.close()
    print(f"Done → {OUT}")

asyncio.run(main())
