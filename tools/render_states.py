#!/usr/bin/env python3
"""render_states.py — load zenaquarium headlessly and capture many UI state screenshots.

Unlocks all content via UNLOCK_ALL so every shop panel, every quest tier, every theme
is visible. Drives setTab/switchFishShop/openSkillWeb to navigate UI states.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

GAME = os.path.expanduser("~/zenaquarium/index.html")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/zen_shots"
os.makedirs(OUT, exist_ok=True)

UNLOCK_ALL = r"""
(() => {
  try {
    playerLevel = 50;
    playerXP = 100000000;
    coins = 100000000;
    totalCoins = 999999999;
    if (typeof boughtCounts === 'object' && boughtCounts !== null) {
      for (const k in TYPES) if (typeof boughtCounts[k] === 'undefined') boughtCounts[k] = 0;
    }
    // Own every theme/floor/bubble/border (cosmetic only — safe)
    ownedThemes = Object.keys(THEMES);
    ownedFloors = Object.keys(FLOORS);
    ownedBubbles = Object.keys(BUBBLES);
    ownedBorders = Object.keys(BORDERS);
    if (typeof ownedFlora !== 'undefined') ownedFlora = ['kelp','coral'];
    // Force a weekly quest into slot 6 for rendering verification
    try {
      generateOrders && generateOrders();
      lastWeeklyTs = Date.now();
      weeklyStreak = 3;
      generateWeeklyQuest && generateWeeklyQuest();
    } catch(e){}
    // Push through save + HUD + level
    // Skip checkEraUnlock — it triggers a 3s announcement watermark
    try { currentEra = 5; } catch(e){}
    try { checkLevel && checkLevel(); } catch(e){}
    try { updateHUD && updateHUD(); } catch(e){}
    try { saveGame && saveGame(); } catch(e){}
    return 'OK';
  } catch(e) { return 'ERR:' + e.message; }
})()
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

# (name, setup JS, wait_ms, viewport_w, viewport_h, full_page)
STATES = [
    ("01_tank_default",   f"({UNLOCK_ALL})",                                                                  3000, 1280, 800,  False),
    ("02_fishshop_buy",   f"({UNLOCK_ALL}); setTab('fishshop')",                                               2000, 1280, 800,  False),
    ("03_fishshop_sell",  f"({UNLOCK_ALL}); setTab('fishshop'); switchFishShop('sell')",                       1800, 1280, 800,  False),
    ("04_fishshop_decor", f"({UNLOCK_ALL}); setTab('fishshop'); switchFishShop('decor')",                      1800, 1280, 800,  False),
    ("05_orders",         f"({UNLOCK_ALL}); setTab('orders')",                                                 1800, 1280, 800,  False),
    ("06_finder",         f"({UNLOCK_ALL}); setTab('finder')",                                                 1800, 1280, 800,  False),
    ("07_social",         f"({UNLOCK_ALL}); setTab('social')",                                                 1800, 1280, 800,  False),
    ("08_skillweb",       f"({UNLOCK_ALL}); openSkillWeb()",                                                   2500, 1280, 800,  False),
    ("09_tank_fullpage",  f"({UNLOCK_ALL})",                                                                  3000, 1280, 1600, True),
    ("10_mobile_portrait",f"({UNLOCK_ALL})",                                                                  2800, 420,  900,  False),
    ("11_mobile_shop",    f"({UNLOCK_ALL}); setTab('fishshop')",                                               2000, 420,  900,  False),
    ("12_mobile_orders",  f"({UNLOCK_ALL}); setTab('orders')",                                                 1800, 420,  900,  False),
    ("13_mobile_skillweb",f"({UNLOCK_ALL}); openSkillWeb()",                                                   2500, 420,  900,  False),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for name, js, wait, w, h, full in STATES:
            page = await browser.new_page(viewport={"width":w,"height":h}, device_scale_factor=2, color_scheme="dark")
            await page.goto(f"file://{GAME}")
            await page.wait_for_load_state("networkidle", timeout=15000)
            try:
                await page.evaluate(CLOSE_MODALS)
            except Exception: pass
            await page.wait_for_timeout(500)
            try:
                result = await page.evaluate(js if not js.startswith("(") else js[1:-1] if False else js)
                # The js above is wrapped in (...) already as expression; evaluate runs as expression
            except Exception as e:
                print(f"  ! {name}: {str(e).splitlines()[0]}")
            await page.wait_for_timeout(wait)
            out = os.path.join(OUT, f"{name}.png")
            await page.screenshot(path=out, full_page=full)
            print(f"  → {out}")
            await page.close()
        await browser.close()
    print(f"Done → {OUT}")

asyncio.run(main())
