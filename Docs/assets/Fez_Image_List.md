# Fez Level - Required Images & File Locations

## Directory Structure

```
images/
├── backgrounds/
│   └── bg_fez.png
├── items/
│   ├── tile_back.png
│   ├── symbol_law.png
│   ├── symbol_astronomy.png
│   ├── symbol_medicine.png
│   ├── symbol_theology.png
│   ├── symbol_mathematics.png
│   ├── symbol_philosophy.png
│   ├── symbol_geography.png
│   └── symbol_literature.png
```

## Complete Image List (9 images total)

### Background Image

**Location**: `images/backgrounds/`

1. **bg_fez.png** - Fez cityscape background (1280x720 pixels)

### Tile & Symbol Images  

**Location**: `images/items/`

1. **tile_back.png** - Generic tile back pattern (120x120 pixels)
2. **symbol_law.png** - Scales of justice (64x64 pixels)
3. **symbol_astronomy.png** - Crescent moon & star (64x64 pixels)
4. **symbol_medicine.png** - Mortar & pestle (64x64 pixels)
5. **symbol_theology.png** - Holy Quran (64x64 pixels)
6. **symbol_mathematics.png** - Geometric pattern (64x64 pixels)
7. **symbol_philosophy.png** - Scroll (64x64 pixels)
8. **symbol_geography.png** - Compass rose (64x64 pixels)
9. **symbol_literature.png** - Quill & inkwell (64x64 pixels)

## Quick Reference - Copy & Paste Names

### For `images/backgrounds/` folder

```
bg_fez.png
```

### For `images/items/` folder

```
tile_back.png
symbol_law.png
symbol_astronomy.png
symbol_medicine.png
symbol_theology.png
symbol_mathematics.png
symbol_philosophy.png
symbol_geography.png
symbol_literature.png
```

## File Naming Rules

- All lowercase
- Use underscores (not spaces or hyphens)
- Must be PNG format with transparency
- No file extension in code references (pgzero adds .png automatically)

## Usage in Code

When referencing in code:

- Background: `"backgrounds/bg_fez"`
- Tile back: `"items/tile_back"`
- Symbols: `"items/symbol_law"`, `"items/symbol_astronomy"`, etc.
