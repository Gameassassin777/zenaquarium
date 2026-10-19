# Zen Aquarium

An aquarium you grow in the browser: fish, breeding, decor, quests, and upgrades, with progress that keeps accruing while you're away. Installs as a home-screen app and works offline.

**Play:** https://calvinslinde.github.io/zenaquarium/

## What's here

- `index.html`: the whole game in one file (about 17,000 lines), plus `sim.js`.
- `manifest.json`, `icon.png`: install-to-home-screen.
- `CHANGELOG.md`: every balance and content change, by version.
- `FEATURE_AUDIT.md`, `CODE_MAP.md`: notes from auditing the game's systems and layout.
- `tools/`, `test.js`, `parse_check.py`: checks used while building.

## Run it locally

Open `index.html` in a browser, or serve the folder:

```
python3 -m http.server 8000
```

Saves live in the browser. Settings has Export and Import for moving a save between devices.

Built with Claude.
