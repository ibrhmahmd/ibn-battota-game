# Code Review - Bug Fixes & Simplifications

## Issues Fixed

### 1. Level Tangier - Redundant Global Declaration

**Line 189**: `items_collected` is declared global in `update()` but never modified there

- Fixed: Removed redundant global declaration

### 2. Level Tangier - Complex Global Statement

**Lines 26-33**: Multi-line global statement with backslashes

- Fixed: Simplified to single line

### 3. Main.py - Empty If Block

**Line 80-81**: Empty if statement that does nothing

- Fixed: Removed unnecessary check

### 4. Division Consistency

**Line 113**: Uses `/` instead of `//` for integer division

- Fixed: Changed to `//` for consistency

## Code Quality Improvements

- Removed unnecessary comments
- Simplified global declarations
- More consistent code style
- Cleaner, more readable structure

All fixes maintain the exact same functionality while making the code clearer for beginners.
