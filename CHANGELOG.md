# Changelog

## v2.7.00 — Premium Polish & Mechanics Depth Overhaul

### Phase 1 — Visitor art completion

- **13 existing visitor branches polished to 9+** on Gemini vision critique (seahare, mantisshrimp, nudibranch, scorpionfish, frogfish, vampiresquid, oarfish, sunfish, lanternfish, velvetray, glasseel, abyssalbloomer, starback).
- **Glassfish bespoke branch** added — translucent body membrane, visible vertebral spine, internal organ silhouette, whisker barbels, caudal fin with rays.
- **Ribbonfish bespoke branch** added — serpentine 16+ segment spine, full-body dorsal membrane, three-phase juvenile→adult color gradient.
- QC tooling extended: `tools/render_fish.py` now renders visitor species into `/tmp/zen_fish_visitors/`.

### Phase 2 — Mechanics rework (11 systems)

Each system deepened existing scaffolding into something that compounds with the rest of the game. Backward-compatible save migration; legacy saves load cleanly.

- **2.1 Personality depth** — `Greedy`, `Playful`, `Loyal`, `Curious`, `Shy` each drive 1+ mechanical hook (food seek radius, tap coin bonus, bond rate, exploration AI, flee response). UI: personality shown in Fish Finder + info popup.
- **2.2 Bonding tiers** — Flat `bonded=3600` replaced with cumulative bond level 1–5. L2 +30% coins, L3 ignores algae penalty, L4 +50% sell price, L5 amplifies personality effect ×2. Decay: 1 tap per 2hr idle. Heart icons L1–L5.
- **2.3 Combo variety** — Beyond tap-speed, added color combo, trait combo, and species-streak jackpot. Stack multiplicatively capped at 3.5×.
- **2.4 Visitor unique abilities** — `def.effect` field. Mantis Shrimp +25% combo, Sea Hare passive algae reduction, Lanternfish +10% coins at night, ~13 species effects.
- **2.5 Era gameplay differentiation** — Per-era passive bonuses (Reef +10% tropical value, Abyss -20% hunger drain, Aurora +50% rare visitors, etc).
- **2.6 Decor synergy** — Themes/floors/bubbles/borders carry `synergy` field (Reef theme +10% tropical, Kelp floor +20% snail speed, Crystal border +30% visitor stay, etc). Bonuses capped at +15%.
- **2.7 Breeding lineage** — `lineage: [{id, type, genes, gen}]` array. Generation-based sell bonus: gen 3 +20%, gen 5 +50%, gen 10+ +200%. Family tree viewer in Aquapedia. Saved to last 5 generations.
- **2.8 Achievement tier escalation** — Each achievement has 4 tiers (I/II/III/IV). Toasts show "Tier II unlocked!" Re-claim rewards on each tier crossing.
- **2.9 Daily reward choices** — 3 cards (coins / 1hr buff / rare resource). Milestone days (7/14/30) add a 4th jackpot card. Streak scales coin value.
- **2.10 Offline events** — 0–2 random events while away (rare visitor, surprise egg, algae bloom debuff, cosmic alignment buff). Pay coins to reroll one bad event on return.
- **2.11 Snail/clam variety** — 3 snail variants (Cleaner/Gilded/Scout) + 2 clam variants (Pearl/Oyster). Each has distinct art, behavior, and mechanical role:
  - Cleaner Snail: algaeMult 1.0, coinMult 1.0 (default)
  - Gilded Snail: algaeMult 0.0, coinMult 3.0 (no cleaning, triple income)
  - Scout Snail: algaeMult 0.2, coinMult 0.5, +15% rare visitor chance each
  - Pearl Clam: coinMult 1.0, no eggs (default)
  - Oyster Clam: coinMult 0.3, 6% rare-egg chance per cycle

### Phase 3 — Verification

- 13-test suite per mechanic (143 tests total) — all passing.
- Cross-system balance: 1800-tick sim under stress load, multipliers stack correctly (2× daily × 0.7 offline = 1.4× net), 0.07ms/frame update with 33 fish + 13 snails + 5 clams.
- Save compat: synthetic v2.6 legacy save migrates without crash. Variant fields default to cleaner/pearl. Achievement IDs migrate to tier dict.
- Performance: helper dispatch (snailVariant/clamVariant/scoutSnailCount/dailyBuffVal/offlineModVal) < 0.4μs/call.
- Art: all 30 catchable + 13 visitor species re-rendered without errors; no drawFish changes in Phase 2.

### Phase 4 — Upgrade-tree balance pass (addicting + enjoyable)

Target payback windows grounded in idle-game design: early 2–5 min, mid 8–20 min, late 25–60 min, endgame 1–3 hr, grail 4 hr+. Variable-ratio reward cadence; no dominant strategy; no upgrade lies (info text matches mechanic); no orphan code; no traps (dead upgrades that never pay back).

- **Info-text truth pass**: heater now actually +25% (was +15% in code, said +25% in UI). Flakes now actually ×2.0 (was ×1.5). Snail_scout description dropped the misleading "small income" line. Magpump description includes Gold Rush.
- **3 new upgrades**:
  - Spectral Lens (L8, Era 2, 120k) — +25% bond XP from every tap.
  - Leviathan Core (L12, Era 4, 5M) — offline income ×3 (wires previously-orphan `leviathancore` flag in calcOffline).
  - Astral Harmonizer (L16, Era 5, 25M) — all era bonuses doubled (delta-amplification: Reef +10% → +20%, Shallows +5% → +10%).
- **Payback curve fixes**:
  - Flakes 1500→800 (L2 fish payback 39 feeds ≈ 2 min at 3s/feed).
  - Singularity 12M→8M, Magpump 4M→2.2M (harmony-window payback 43 feeds ≈ 22 min).
  - Bioreactor 600k→350k, Aurastone 1.2M→850k, Ethkey 5M→3.5M.
- **Variant tuning**:
  - Scout Snail: coinMult 0.5→1.0 (no income penalty, just algae penalty — was strictly worse than Cleaner for 95% of players).
  - Oyster Clam: eggChance 6%→4% (preserves rare-egg role without flooding late game).
- **Magpump**: now applies during Gold Rush too (was Harmony-only, halving its trigger window).
- **Heater + Flakes mastery**: heater base 1.25 + 0.08/sw level, flakes base 2.0 + 0.25/sw level.
- **Verification**: 14-test Playwright suite covering costs, era-gating, info-truth (via source inspection), variant data, multiplier truth, bond boost, offline ×3, era amplification, save round-trip, legacy backward-compat, payback curves at L2/L12/L14.

### Out of scope (deferred to v2.8+)

- Multiplayer / leaderboards
- Audio/music overhaul
- Major UI restructure
- Mobile-native port
