#!/usr/bin/env python3
"""render_fish.py — render specific fish/visitor species in isolation for art QC.

Generates one screenshot per species at high resolution so each can be
individually critiqued by Gemini vision.

Usage:
  python3 render_fish.py                              # default: render ALL catchable → /tmp/zen_fish
  python3 render_fish.py /out/dir                     # render all catchable → custom dir
  python3 render_fish.py /out/dir guppy betta         # render only specific catchable species
  python3 render_fish.py /tmp/zen_visitors --visitors # render ALL visitors
  python3 render_fish.py /tmp/zen_visitors glassfish ribbonfish  # auto-detect: visitor keys
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

GAME = os.path.expanduser("~/zenaquarium/index.html")
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "/tmp/zen_fish"
os.makedirs(OUT, exist_ok=True)

ALL_CATCHABLE = [
    "guppy", "tetra", "goldfish", "betta", "angelfish", "discus",
    "jellyfish", "octopus", "turtle", "whaleshark", "narwhal", "lionfish",
    "seahorse", "idol", "mantaray", "cuttlefish", "pufferfish", "dragoneel",
    "seadragon", "colossalsquid",
    "viperfish", "gulper", "anglerfish", "isopod", "vampiresquid",
    "oarfish", "megamouth", "frilledshark", "siphonophore", "leviathan",
]

ALL_VISITORS = [
    "seahare", "mantisshrimp", "nudibranch", "scorpionfish", "frogfish",
    "sunfish", "lanternfish", "velvetray", "glasseel",
    "abyssalbloomer", "starback", "glassfish", "ribbonfish",
    # 'vampiresquid' and 'oarfish' share art with catchable; render once via catchable path
]

# Parse args: --visitors flag forces visitor mode for all args after out_dir
FORCE_VISITORS = "--visitors" in sys.argv
args_species = [a for a in sys.argv[2:] if not a.startswith("-")]

if FORCE_VISITORS and not args_species:
    SPECIES = ALL_VISITORS
elif args_species:
    SPECIES = args_species
else:
    SPECIES = ALL_CATCHABLE

# Auto-detect mode per species: visitor if in ALL_VISITORS, else catchable
def is_visitor(sp):
    return sp in ALL_VISITORS or (FORCE_VISITORS and sp not in ALL_CATCHABLE)

# JS template: spawn one fish of given type at center, lock camera, hide UI
def spawn_js(species):
    return f"""
(() => {{
  try {{
    fishList.length = 0;
    seaweeds.length = 0;
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
    f.scale = 5.0;
    f.hunger = 100;
    f.bonded = 0;
    return 'OK';
  }} catch(e) {{ return 'ERR:' + e.message + ' // ' + (e.stack||''); }}
}})()
    """

def spawn_js_visitor(key):
    """Spawn a visitor by pushing directly to visitorList with key+def."""
    return f"""
(() => {{
  try {{
    visitorList.length = 0;
    fishList.length = 0;
    seaweeds.length = 0;
    snails.length = 0;
    clams.length = 0;
    particles.length = 0;
    marineSnow.length = 0;
    let _vs;
    try {{ _vs = VISITOR_SPECIES; }} catch(_) {{ _vs = null; }}
    if (!_vs || !_vs[{repr(key)}])
      return 'ERR: no VISITOR_SPECIES entry for ' + {repr(key)} + ' (VISITOR_SPECIES=' + (typeof _vs) + ')';
    const def = _vs[{repr(key)}];
    const v = {{
      id: 'v_qc_' + Date.now(),
      key: {repr(key)},
      def: def,
      type: 'guppy',
      x: W / 2,
      y: H / 2,
      vx: 0.4, vy: 0,
      phase: Math.random() * Math.PI * 2,
      timer: 0, eat: 0,
      hunger: 100,
      age: 60000,
      scale: 5.0,
      bonded: 0,
      genes: {{ c1:[def.c1,def.c1], c2:[def.c2,def.c2], trait:['active','active'], szMod:1.0 }},
      isRare: false,
      isVisitor: true,
      trust: 50, trustTimer: 999999,
      spooked: false, spookedTimer: 0,
      abyssal: !!def.abyssal,
      isEcho: false,
      echoCopy: null,
      _sz: def.sz,
      birthTime: Date.now(),
      name: def.name
    }};
    visitorList.push(v);
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
            visitor_mode = is_visitor(species)
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
                spawn_fn = spawn_js_visitor if visitor_mode else spawn_js
                result = await page.evaluate(spawn_fn(species))
                if isinstance(result, str) and result.startswith("ERR"):
                    print(f"  ! {species} ({'visitor' if visitor_mode else 'catchable'}): {result[:300]}")
            except Exception as e:
                print(f"  ! {species}: {str(e)[:200]}")
            await page.wait_for_timeout(2000)
            try:
                pre_shot = await page.evaluate("JSON.stringify({sw:seaweeds.length, part:particles.length, ms:marineSnow.length, fl:fishList.length, vl:visitorList.length})")
                print(f"    [state] {pre_shot}")
            except Exception as e:
                print(f"    [state-err] {str(e)[:150]}")
            out = os.path.join(OUT, f"{species}.png")
            await page.screenshot(path=out)
            print(f"  → {out} ({'visitor' if visitor_mode else 'catchable'})")
            await page.close()
        await browser.close()
    print(f"Done → {OUT}")

asyncio.run(main())
