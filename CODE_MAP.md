# Zen Aquarium Code Map

> Systematic UI reference for index.html (8072 lines)
> Generated for UI beautification pass

---

## 1. Global State

### Core Player Variables

| Variable | Line | Purpose |
|----------|------|---------|
| `playerLevel` | 1288 | Current player level (1-50) |
| `playerXP` | 1288 | Total accumulated XP |
| `coins` | 1289 | Current spendable coins |
| `totalCoins` | 1288 | Lifetime coins earned (stat tracking) |
| `algae` | 1290 | Tank pollution percentage (0-100) |
| `baseMaxFish` | 1290 | Base fish capacity (before bonuses) |
| `fishList` | 1289 | Array of fish objects in tank |
| `foodList` | 1289 | Array of food particles |
| `bubbles` | 1289 | Array of bubble particles |
| `seaweeds` | 1289 | Array of seaweed decor objects |
| `snails` | 1289 | Array of snail cleaner objects |
| `particles` | 1289 | Array of effect particles |
| `clams` | 1289 | Array of clam objects |
| `eggs` | 1289 | Array of unhatched eggs |
| `marineSnow` | 1289 | Ambient particle array |

### Ownership Arrays

| Variable | Line | Purpose |
|----------|------|---------|
| `ownedThemes` | 1370 | Owned water themes (starts with 'default') |
| `ownedFloors` | 1370 | Owned substrate types (starts with 'default') |
| `ownedBubbles` | 1370 | Owned bubble styles (starts with 'default') |
| `ownedBorders` | 1370 | Owned tank borders (starts with 'none') |
| `ownedFlora` | 1417 | Owned flora types (seaweed, grass, kelp, coral) |
| `activeFlora` | 1418 | Subset of ownedFlora currently visible |
| `boughtCounts` | 1419 | Purchase count per fish type (for pricing) |

### System State

| Variable | Line | Purpose |
|----------|------|---------|
| `time` | 1290 | Game tick counter (60 ticks/sec) |
| `fid` | 1290 | Fish ID counter (auto-increment) |
| `currentEra` | 1304 | Current era (0=Tidepool, 5=Abyss) |
| `questStreak` | 1366 | Consecutive daily quest completions |
| `_openQuests` | 1366 | Set of expanded quest indices |
| `claimedCodes` | 1367 | Set of redeemed friend codes |
| `isHarmony` | 1300 | Harmony mode state (double rewards) |
| `combo` | 1296 | Current combo multiplier |
| `surgingType` | 1512 | Currently surging fish type in market |
| `marketRates` | 1511 | Dynamic market multiplier per fish type |

---

## 2. Catalogs

### Fish Types (TYPES)

**Location:** Lines 1393-1422 (30 species)

```javascript
const TYPES = {
  guppy:   { name:'Guppy',   icon:'🐟', c1:'#38bdf8', c2:'#0284c7', sz:18, cost:50,  val:1, req:1 },
  neon:    { name:'Neon',    icon:'🐠', c1:'#67e8f9', c2:'#a855f7', sz:24, cost:100, val:2, req:1 },
  // ... 30 total species
}
```

**Properties per fish:** `name`, `icon`, `c1` (primary color), `c2` (secondary color), `sz` (size), `cost` (shop price), `val` (value), `req` (level req)

---

### Decor Catalogs

| Catalog | Lines | Item Count | Location |
|---------|-------|------------|----------|
| THEMES | 1456-1469 | 5 themes | Water gradient backgrounds |
| FLOORS | 1470-1483 | 5 substrates | Tank floor textures |
| BUBBLES | 1484-1494 | 4 styles | Bubble particle styles |
| BORDERS | 1495-1506 | 5 borders | Canvas frame borders |

---

### Upgrade Catalog (UPGRADES)

**Lines:** 1428-1455

Key upgrades:
- `bioreactor`: Algae generation multiplier
- `filter`: Algae reduction
- `autofeed`: Automatic feeding
- `snail`, `clam`: Adds cleaner creatures
- `kelp`, `coral`: Flora unlocks
- `tank`: +3 fish capacity per level

---

## 3. Save/Load System

### Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `buildSave()` | 1856-1877 | Serializes all state to JSON object |
| `saveGame()` | 1878 | Persists buildSave() to localStorage |
| `loadSave()` | 1880-1895 | Reads from localStorage (with legacy key fallback) |
| `applyState(s)` | 1896-1975 | Deserializes save into global variables |

**Save Key:** `MASTER_KEY` (line ~8470)

**Legacy Keys Checked:** Array of old save keys for migration

---

## 4. Leveling System

### Constants

| Constant | Lines | Purpose |
|----------|-------|---------|
| `XP_THRESHOLDS` | 5136-5142 | XP needed for each level (50 levels) |
| `LEVEL_UNLOCKS` | 5143-5170 | Features unlocked per level |
| `CELEBRATION_LEVELS` | 5171 | Levels triggering special modal (10,15,20,25,30,40,50) |
| `ERA_REQ_LEVELS` | 5226 | Levels required for each era (0,5,10,15,20) |

### Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `giveXP(base)` | 5173-5180 | Adds XP with multipliers (harmony, combo, fish bonus) |
| `checkLevel()` | 5182-5224 | Checks level-up, shows modal, unlocks features |
| `checkEraUnlock()` | 5225-5240 | Checks if new era should be announced |
| `showEraAnnouncement(eraIdx)` | 5241-5252 | Displays era unlock modal |

---

## 5. Tab System

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `setTab(t)` | 5410-5426 | Switches main nav tab, builds panel | `.panel.open`, `.panel.full` |
| `buildPanel(t)` | 5433-5437 | Routes to specific builder functions | - |
| `switchFishShop(tab)` | 6417-6430 | Switches Buy/Sell/Decor subtabs | `.tabbtn.active` |
| `openSkillWeb()` | 7344-7376 | Opens skill web overlay | `#skill-web-overlay.open` |
| `closeAll()` | 6018-6027 | Closes all panels | `.panel` (removes open) |

**Tab IDs:** `fishshop`, `orders`, `social`, `finder`

---

## 6. Shop Builders

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `buildShop()` | 6461-6489 | Renders fish buy panel | `.card`, `.buyable`, `.full` |
| `buildMarket()` | 2150-2217 | Renders live fish market | `.card`, `.buyable` |
| `buildDecor()` | 6360-6415 | Renders Decor/Themes/Floors panel | `.card`, `.buyable`, `.equipped` |
| `buildSupplies()` | ~6512-6560 | Renders upgrades panel | `.card`, `.locked`, `.full` |

**DOM IDs Written:**
- `#fcards` → fish cards
- `#ucards` → upgrade cards  
- `#acc-themes`, `#acc-substrates`, etc → accordion sections

---

## 7. Quest System

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `buildOrders()` | 6994-7138 | Renders quest list | `.ocard`, `.ocard.expanded`, `.odone`, `.oclaimed` |
| `generateOrders()` | (search) | Creates 5 daily quests | - |
| `toggleQuest(i, el)` | (in buildOrders) | Expands/collapses quest card | `.ocard.expanded` |

### Quest Card CSS Classes

| Class | Lines | Purpose |
|-------|-------|---------|
| `.ocard` | 169 | Base quest card container |
| `.ocard.expanded` | 170 | Shows quest details |
| `.ocard.odone` | 171 | Completed quest (green) |
| `.ocard.oclaimed` | 172 | Already claimed (grayed) |
| `.ocard.ql` | 329 | Legend tier quest (purple) |
| `.ocard.q-daily` | 179 | Elite daily quest (purple glow) |
| `.opbg` | 256 | Progress bar background |
| `.opf` | 257 | Progress bar fill |
| `.opf.odone` | 258 | Completed progress (green) |

**DOM ID:** `#olist`

---

## 8. Fish Finder

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `buildFishFinder()` | 5448-5567 | Renders sortable fish list | `.finder-card` |

**DOM ID:** `#flist`

**Renders:** Each fish with name, species, stats, edit/gift buttons

---

## 9. Social System

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `buildSocial()` | 6570-6702 | Renders social/stats panel | `.ocard`, `.srow`, `.wrow` |

**Sections Rendered:**
- System info & reset button
- Update checker
- General statistics
- Quest achievements
- Fish collection (with rename/gift)
- Friend code display
- Code redemption
- Settings (tutorials, export/import)

**DOM IDs:** `#socdiv`, `#mycode`, `#sstreak`, `#sorders`, `#stotal`, `#scodes`, `#m-list`, `#gift-list`

---

## 10. Skill Web

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `openSkillWeb()` | 7344-7376 | Opens skill tree overlay | `#skill-web-overlay.open` |
| `closeSkillWeb()` | 7380-7397 | Closes overlay | removes `.open` |
| `swResizeCanvas()` | 7403-7410 | Resizes skill canvas | - |
| `swStartLoop()` | (search) | Starts skill web animation | - |

**Skill Web DOM Elements:**
- `#skill-web-overlay` → Modal container
- `#swc` → Skill canvas
- `#sw-mini` → Minimap canvas
- `#sw-era` → Era label
- `#sw-np-inner` → Node purchase panel content

**CSS Classes:**
- `.sw-np-row` → Node row (line 513)
- `.sw-np-buy` → Buy button (line 514)
- `.sw-np-req` → Requirement text (line 517)

---

## 11. HUD/Topbar

### Functions

| Function | Lines | Purpose | Updates |
|----------|-------|---------|---------|
| `updateHUD()` | 1986-2030 | Refreshes all topbar values | Coins, level, fish count, water, XP bar, era |

**DOM Elements Updated:**
- `#cv` → Coins display
- `#lvl` → Level display
- `#wv` → Water quality %
- `#fv` → Fish count (X/Y format)
- `#xp-bar` → XP progress bar (width %)
- `#era-val` → Current era name

### HUD CSS Classes

| Class | Lines | Purpose |
|-------|-------|---------|
| `.dash` | 114 | Main topbar container |
| `.dash.harmony` | 115 | Harmony mode (golden glow) |
| `.stat` | 116 | Individual stat column |
| `.slbl` | 117 | Stat label (COINS, LEVEL, etc) |
| `.sval` | 118 | Stat value display |
| `.sval.vl` | 120 | Value highlight (accent color) |
| `.cbar` | 153 | Combo bar background |
| `.cfill` | 154 | Combo bar fill |
| `.xpb` | 156 | XP bar container |
| `.xpf` | 157 | XP bar fill |

**XP Bar Styling:** Dynamic gradient based on progress (line 2005-2015)

---

## 12. Modal System

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `showWelcome(r)` | 2081-2088 | Shows welcome/offline rewards modal | `.modal.show` |
| `showDailyModal()` | 2101-2107 | Shows daily streak modal | `.modal.show` |

### Modal CSS Classes

| Class | Lines | Purpose |
|-------|-------|---------|
| `.modal` | 268 | Modal overlay (fixed, inset:0) |
| `.modal.show` | 269 | Visible state (opacity:1) |
| `.mbox` | 270 | Modal content box |
| `.msub` | 272 | Modal subtitle text |
| `.mbtn` | 273 | Modal button |
| `.mbtn.gold` | (search) | Gold claim button variant |

**Modal Content HTML:** Injected directly into `.mbox`

---

## 13. Daily Reward System

### Functions

| Function | Lines | Purpose | Emits Classes |
|----------|-------|---------|----------------|
| `needsDaily()` | 2095-2100 | Checks if daily available | - |
| `claimDaily()` | 2108-2119 | Claims daily reward | - |
| `collectOffline()` | 2089-2094 | Calculates offline earnings | - |

### Daily Reward CSS Classes

| Class | Lines | Purpose |
|-------|-------|---------|
| `.drbox` | 280 | Daily reward card container |
| `.dramt` | 281 | Reward amount (large gold text) |

**State Variables:**
- `dailyStreak` → Consecutive days claimed
- `lastDailyTs` → Timestamp of last claim
- `offlinePend` → Pending offline earnings object

---

## 14. Canvas/Tank Rendering

### Functions

| Function | Lines | Purpose | Key Operations |
|----------|-------|---------|----------------|
| `loop(frameTs)` | 4304-5020 | Main animation loop | Clears canvas, updates all entities, draws all |
| `drawFish(f)` | 2757-3576 | Renders single fish | Body, fins, eyes, effects, species variants |
| `drawFishName(f)` | 3975-3999 | Renders fish name tag | Tooltip-style text |
| `drawDecor()` | (in loop) | Renders tank decorations | Calls flora, floor, border renderers |
| `drawSnail(s)` | 2692-2733 | Renders snail cleaner | Shell, body, eye |
| `drawEye()` | 2734-2739 | Renders eye graphic | Used by fish/snail |
| `drawExclamation()` | 2740-2744 | Renders warning icon | Low hunger indicator |
| `drawHeart()` | 2748-2756 | Renders heart icon | Bonded fish indicator |

### Rendering Pipeline (loop function)

**Lines 4304-5020**

1. **Delta-time calculation** (4304-4322): Cap at 50ms, accumulate for 60fps ticks
2. **Update phase** (per tick):
   - `updateEco()` → Algae, coin generation (2260-2287)
   - `updateFish(f)` per fish → Movement, hunger, aging (2436-2622)
   - `updateSnail(s)` per snail → Algae cleaning (2663-2691)
   - `checkMilestones()` → Quest progress (5400-5409)
   - `updateEliteTimerUI()` → Visitor timer (4010-4027)
3. **Draw phase**:
   - Clear canvas (4345)
   - Draw water gradient with algae tint (4348-4385)
   - Draw light rays (4388-4456)
   - Draw substrate/floor (4870-4887)
   - Draw flora (4535-4588)
   - Draw decorations (clams, 4703-4745)
   - Draw all fish (4798-4799)
   - Draw all fish names (4799)
   - Draw visitor echo fish (4803)
   - Draw bubbles (lines ~)
   - Draw food (lines ~)
   - Draw border (4971-5007)

### Fish Scale Calculation

**Line 4609-4612:**
```javascript
const sSize = TYPES[f.type].sz * f.scale * (f.genes.szMod||1) * 0.85;
```

**Global level scale** (line 1390):
```javascript
const getGlobalLevelScale = () => Math.max(0.7, 1.0 - (playerLevel - 1) * 0.006);
```

---

## 15. CSS Class Glossary

### Navigation & Tabs

| Class | Lines | Purpose |
|-------|-------|---------|
| `.nb` | 160 | Nav button (bottom tab bar) |
| `.tabbtn` | 265 | Tab button (Shop subtabs) |
| `.tabbtn.active` | 265 | Active tab state |

### Cards & Panels

| Class | Lines | Purpose |
|-------|-------|---------|
| `.panel` | 184 | Bottom panel container (slides up) |
| `.panel.open` | 184 | Visible state |
| `.panel.full` | 184 | Expanded state |
| `.card` | 207 | Shop item card |
| `.card.buyable` | 209 | Affordable item (green glow) |
| `.card.equipped` | 210 | Currently equipped item (cyan glow) |
| `.card.full` | 211 | Maxed out/locked (dimmed) |
| `.card.locked` | 213 | Level-locked (semi-transparent) |
| `.finder-card` | (buildFishFinder) | Fish list item |

### Card Content Elements

| Class | Lines | Purpose |
|-------|-------|---------|
| `.ci` | 246 | Card icon (large emoji) |
| `.cn` | 247 | Card name |
| `.cd` | 248 | Card description |
| `.cpr` | 249 | Card price (gold) |
| `.cown` | 250 | Ownership count |
| `.cbtn` | 309 | Small action button |
| `.cbtn2` | 262 | Claim button (green) |

### Quest Cards

| Class | Lines | Purpose |
|-------|-------|---------|
| `.ocard` | 169 | Order/quest card |
| `.ohead` | 252 | Quest header (icon + title) |
| `.oico` | 253 | Quest icon |
| `.odesc` | 254 | Quest description |
| `.orew` | 255 | Quest reward text |
| `.opbg` | 256 | Progress bar background |
| `.opf` | 257 | Progress bar fill |
| `.opf.odone` | 258 | Completed progress (green) |
| `.ofoot` | 259 | Quest footer |
| `.ocnt` | 260 | Quest counter text |
| `.o-details` | 173 | Expanded quest details |
| `.o-chevron` | 175 | Expand/collapse arrow |
| `.o-reward-item` | 178 | Reward line item |
| `.tier-badge` | 324 | Tier label (EASY/MED/HARD/LEGEND) |

### Buttons

| Class | Lines | Purpose |
|-------|-------|---------|
| `.hbtn` | 133 | Header action button |
| `.mbtn` | 273 | Modal button |
| `.rbtn` | 293 | Redeem/code button |

### Accordion (Skill Web / Decor)

| Class | Lines | Purpose |
|-------|-------|---------|
| `.acc-hd` | 194 | Accordion header |
| `.acc-hd-title` | 196 | Accordion title |
| `.acc-hd-sub` | 197 | Accordion subtitle |
| `.acc-arrow` | 198 | Expand/collapse arrow |
| `.acc-body` | 200 | Accordion body (expandable) |
| `.acc-body-inner` | 202 | Accordion inner content |

### Section Headers

| Class | Lines | Purpose |
|-------|-------|---------|
| `.sechead` | 204 | Section header text |
| `.pt` | 190 | Panel title |

### Statistics Rows

| Class | Lines | Purpose |
|-------|-------|---------|
| `.srow` | 318 | Stats row (label + value) |
| `.wrow` | 276 | Widget row (e.g., code box) |

### Modals

| Class | Lines | Purpose |
|-------|-------|---------|
| `.modal` | 268 | Modal overlay |
| `.mbox` | 270 | Modal content box |
| `.msub` | 272 | Modal subtitle |

### Daily Rewards

| Class | Lines | Purpose |
|-------|-------|---------|
| `.drbox` | 280 | Daily reward box |
| `.dramt` | 281 | Daily reward amount (large) |
| `.sdots` | 282 | Streak dots |
| `.sd` | 283 | Individual streak dot |

### Code Box

| Class | Lines | Purpose |
|-------|-------|---------|
| `.codebox` | 287 | Code display box |
| `.cbig` | 288 | Code text (large) |
| `.chint` | 289 | Code hint text |
| `.copybtn` | 290 | Copy button |

### Input Elements

| Class | Lines | Purpose |
|-------|-------|---------|
| `.irow` | 291 | Input row container |
| `.cinput` | 292 | Code input field |

### Effects & Animations

| Class | Lines | Purpose |
|-------|-------|---------|
| `.ft` | 305 | Floating text (coin popups) |
| `.gift-fish-row` | 319 | Fish gift row in social |
| `.giftbtn` | 321 | Gift action button |

### Aquapedia (Book)

| Class | Lines | Purpose |
|-------|-------|---------|
| `.aq-card` | 338 | Aquapedia entry card |
| `.aq-stamp` | 339 | Color band stamp |
| `.aq-stamp-pop` | 342 | Stamp pop animation |
| `.aq-prismatic-badge` | 343 | Prismatic badge glow |
| `.aq-wax-seal` | 474 | Decorative wax seal |
| `.aq-ink-blot` | 482 | Ink blot effect |
| `.aq-stamp-seal` | 486 | Stamp seal |
| `.aq-page-num` | 494 | Page number |
| `.aq-fish-preview` | 497 | Fish preview canvas |

### Book Navigation

| Class | Lines | Purpose |
|-------|-------|---------|
| `.book-close` | 410 | Close book button |
| `.book-nav-btn` | 441 | Book navigation button |
| `.book-page-flip-out-left` | 460 | Page flip animation (left) |
| `.book-page-flip-in-right` | 461 | Page flip animation (right) |
| `.book-page-flip-out-right` | 462 | Page flip animation (right) |
| `.book-page-flip-in-left` | 463 | Page flip animation (left) |
| `.book-page-corner` | 467 | Page corner graphic |

### Skill Web

| Class | Lines | Purpose |
|-------|-------|---------|
| `.sw-np-row` | 513 | Node panel row |
| `.sw-np-buy` | 514 | Buy button |
| `.sw-np-req` | 517 | Requirement text |

### Quest Streak

| Class | Lines | Purpose |
|-------|-------|---------|
| `.ostreak` | 348 | Streak indicator card |
| `.q-total` | 349 | Quest total label |

### Tier Badges

| Class | Lines | Purpose |
|-------|-------|---------|
| `.tier-badge` | 324 | Tier badge base |
| `.tbg-easy` | 325 | Easy tier (green) |
| `.tbg-med` | 326 | Medium tier (yellow) |
| `.tbg-hard` | 327 | Hard tier (red) |
| `.tbg-legend` | 328 | Legend tier (purple) |

### Value Colors

| Class | Lines | Purpose |
|-------|-------|---------|
| `.v-good` | 120 | Good status (green) |
| `.v-warn` | 121 | Warning status (red) |
| `.v-money` | 122 | Money/gold color |
| `.v-harmony` | 131 | Harmony mode (gold glow) |

### Trait Icons

| Class | Lines | Purpose |
|-------|-------|---------|
| `.trait-icon` | 312 | Fish personality trait badge |

### Claim Animation

| Class | Lines | Purpose |
|-------|-------|---------|
| `.claim-ready` | 330 | Pulsing claim button |

### Responsive (Media Queries)

| Class | Lines | Purpose |
|-------|-------|---------|
| `.pscroll` | 190 | Panel scroll container |
| `.ph` | 190 | Panel header (draggable) |
| `.xbtn` | 193 | Close panel button |

---

## Quick Reference: Common UI Tasks

### Change Fish Sizing
**Location:** `drawFish()` function (line 2757), specifically line 4609:
```javascript
const sSize = TYPES[f.type].sz * f.scale * (f.genes.szMod||1) * 0.85;
```
**Also:** `getGlobalLevelScale()` at line 1390 affects all fish globally

### Modify XP Bar Colors
**Location:** `updateHUD()` function, lines 2005-2015

### Change Quest Card Styling
**Location:** CSS lines 169-172 (`.ocard` base classes)

### Update Topbar Layout
**Location:** CSS lines 114-157 (`.dash`, `.stat`, `.slbl`, `.sval`)

### Modify Modal Appearance
**Location:** CSS lines 268-273 (`.modal`, `.mbox`)

### Change Card Grid Layout
**Location:** CSS line 206 (`.cards` → `grid-template-columns`)

### Add/Remove Shop Tabs
**Location:** `switchFishShop()` at line 6417, plus HTML buttons at lines 967-969

### Modify Fish Render Style
**Location:** `drawFish()` at line 2757 - contains all species rendering logic

### Change Water/Background Colors
**Location:** `_drawThemeBackground()` at line 4045, and `THEMES` catalog at line 1456

### Adjust Panel Slide Animation
**Location:** CSS line 184 (`.panel` → `transform` transition timing)

### Modify Skill Web Node Styling
**Location:** CSS lines 513-517 (`.sw-np-*` classes)

### Change Daily Reward Display
**Location:** `showDailyModal()` at line 2101, CSS lines 280-281

---

## File Structure Overview

```
index.html (8072 lines)
├── 1-1059: CSS Styles
│   ├── 114-335: Core UI (dash, cards, modals, buttons)
│   ├── 338-508: Aquapedia (book) styles
│   ├── 510-540: Skill web styles
│   └── 542-843: Responsive queries
├── 1060-1284: PWA setup & constants
├── 1285-1398: Global state declarations
├── 1399-1647: Color & genetics systems
├── 1648-1855: Save/load & helpers
├── 1856-2080: Save/load functions
├── 2081-2203: Daily rewards & offline
├── 2204-2435: Market & economy
├── 2436-2624: Fish update logic
├── 2625-2756: Decor & snails
├── 2757-4299: Drawing functions
├── 4304-5407: Main loop & interactions
├── 5408-6038: Panel & tab system
├── 6039-6326: Book (Aquapedia) system
├── 6327-6569: Shop builders
├── 6570-6897: Social & codes
├── 6898-7342: Quest system
├── 7343-8093: Skill web system
├── 8094-8498: Animation loop & boot
└── 8499-end: Final initialization
```

---

## End of Document

**Generated:** 2026-07-01
**Purpose:** UI beautification reference
**File:** /Users/calvinslinde/zenaquarium/index.html
**Total Lines:** 8072
