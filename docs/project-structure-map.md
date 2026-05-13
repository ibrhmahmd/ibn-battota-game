# Ibn Battota Game - Technical Map

## File Tree
```
ibn-battota-game/
├── main.py                    [ENTRY POINT] Screen router, event dispatcher
├── start_screen.py            [START] Menu with play button
├── world_map.py               [HUB] 13 cities, character navigation
├── mission_overlay.py         [SYSTEM] Mission briefing overlay
├── levels/
│   ├── level_tangier.py       [TEMPLATE] Fully detailed level implementation
│   ├── level_fez.py           
│   ├── level_cairo.py         
│   ├── level_damascus.py      
│   └── level_timbuktu.py      
├── images/
│   ├── backgrounds/           Map, level BGs, city icons, UI
│   ├── characters/            Player sprites
│   ├── items/                 Collectibles, platforms, UI elements
│   ├── ui/                    Buttons, icons
│   └── levels_texts/          Mission briefing text images
├── music/                     [NOT ANALYZED] Audio tracks
└── __pycache__/
```

## Quick Navigation Map

### To add/modify a level:
→ `levels/level_[CITY].py` + relevant assets in `images/`

### To change world map:
→ `world_map.py` (CITIES_CONFIG list, 13 entries)

### To modify game flow:
→ `main.py` (screen state transitions)

### To add mission briefing:
→ `mission_overlay.py` + `images/levels_texts/text_[CITY].png`

## Key Constants (main.py)
- WIDTH = 1280
- HEIGHT = 720
- Mute button pos: (1220, 60)

## Reference: Tangier Level Architecture
- 10 platforms arranged as jumping puzzle
- 10 collectible items
- Leaf particle effects
- Victory seal when all items collected
- Back button to return to map

---

## Quick Commands
| Task | Location |
|------|----------|
| Add new city to map | `world_map.py` line ~4 |
| Add level completion logic | `main.py` on_key_down() |
| Modify physics | `level_[CITY].py` line ~11 |
| Change UI button position | Main file line ~ 12 |
