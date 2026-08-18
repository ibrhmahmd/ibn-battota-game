import pygame
import os
import random

os.environ["SDL_VIDEODRIVER"] = "windib"

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ibn Battota - Screenshot Capture")

ASSETS = os.path.join(os.path.dirname(__file__), "images")
SCREENSHOTS = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS, exist_ok=True)


def asset(name):
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(ASSETS, name + ext)
        if os.path.exists(path):
            return path
    return os.path.join(ASSETS, name + ".png")


def load(name):
    return pygame.image.load(asset(name)).convert_alpha()


def save(surface, name):
    path = os.path.join(SCREENSHOTS, name)
    pygame.image.save(surface, path)
    print(f"  Saved: {name}")


def draw_text(surface, text, pos, size=40, color=(255, 255, 255), outline=True):
    font = pygame.font.SysFont("arial", size, bold=True)
    if outline:
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx == 0 and dy == 0:
                    continue
                out = font.render(text, True, (0, 0, 0))
                surface.blit(out, (pos[0] + dx, pos[1] + dy))
    txt = font.render(text, True, color)
    surface.blit(txt, pos)


def draw_text_center(surface, text, center, size=40, color=(255, 255, 255), outline=True):
    font = pygame.font.SysFont("arial", size, bold=True)
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=center)
    if outline:
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                out = font.render(text, True, (0, 0, 0))
                surface.blit(out, rect.move(dx, dy))
    surface.blit(txt, rect)


def capture_start_screen():
    print("Capturing: Start Screen")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load("backgrounds/start_screen_background")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))
    btn = load("ui/start_btn")
    btn_rect = btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90))
    surf.blit(btn, btn_rect)
    save(surf, "01_start_screen.png")


def capture_world_map():
    print("Capturing: World Map")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load("backgrounds/map")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))

    CITIES_CONFIG = [
        ("tangier", (106, 420)),
        ("fez", (32, 490)),
        ("granada", (75, 300)),
        ("istanbul", (390, 350)),
        ("cairo", (480, 525)),
        ("damascus", (600, 434)),
        ("baghdad", (773, 470)),
        ("medina", (640, 525)),
        ("mecca", (720, 577)),
        ("persia", (853, 455)),
        ("delhi", (1226, 535)),
        ("timbuktu", (53, 680)),
        ("beijing", (1173, 210)),
    ]

    for name, pos in CITIES_CONFIG:
        icon = load(f"backgrounds/icons/{name}")
        icon_rect = icon.get_rect(center=pos)
        surf.blit(icon, icon_rect)
        label = name.replace("_", " ").title()
        font = pygame.font.SysFont("arial", 18, bold=True)
        txt = font.render(label, True, (139, 69, 19))
        txt_rect = txt.get_rect(center=(pos[0], pos[1] - 40))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                out = font.render(label, True, (255, 215, 0))
                surf.blit(out, txt_rect.move(dx, dy))
        surf.blit(txt, txt_rect)

    character = load("characters/character")
    char_rect = character.get_rect(center=(150, 600))
    surf.blit(character, char_rect)

    mute = load("ui/music_on")
    surf.blit(mute, mute.get_rect(center=(WIDTH - 60, 60)))

    save(surf, "02_world_map.png")


def capture_level_with_mission(level_name, bg_name, bg_ext="png"):
    print(f"Capturing: {level_name.title()} - Mission Briefing")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load(f"backgrounds/{bg_name}")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surf.blit(overlay, (0, 0))

    try:
        frame = load("items/mission_briefing")
        frame_rect = frame.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surf.blit(frame, frame_rect)
    except:
        pass

    try:
        text_img = load(f"levels_texts/text_{level_name}")
        text_rect = text_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surf.blit(text_img, text_rect)
    except:
        pass

    mute = load("ui/music_on")
    surf.blit(mute, mute.get_rect(center=(WIDTH - 60, 60)))

    save(surf, f"03_{level_name}_mission.png")


def capture_tangier_gameplay():
    print("Capturing: Tangier - Gameplay")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load("backgrounds/bg_tangier")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))

    platform = load("items/platforms/platform")
    platform_positions = [
        (300, 600), (600, 550), (900, 500), (450, 450),
        (750, 400), (1100, 370), (450, 265), (950, 220),
        (1020, 630), (1220, 630),
    ]
    for pos in platform_positions:
        surf.blit(platform, platform.get_rect(center=pos))

    collectible_items = [
        ("items/collectibles/prayer_mat", (200, 630)),
        ("items/collectibles/leather_sandals", (450, 410)),
        ("items/collectibles/compass", (600, 510)),
        ("items/collectibles/holy_quran", (750, 360)),
        ("items/collectibles/woolen_djellaba", (800, 630)),
        ("items/collectibles/water_skin", (900, 460)),
        ("items/collectibles/silver_dirhams", (300, 560)),
        ("items/collectibles/oil_lamp", (500, 630)),
        ("items/collectibles/travel_documents", (1080, 550)),
        ("items/collectibles/inkwell_and_kalam", (1100, 330)),
    ]
    for img_name, pos in collectible_items:
        item = load(img_name)
        surf.blit(item, item.get_rect(center=pos))

    character = load("characters/character")
    surf.blit(character, character.get_rect(center=(150, 500)))

    back = load("ui/back_btn")
    surf.blit(back, back.get_rect(center=(80, 50)))

    draw_text(surf, "Items: 3/10", (20, 100), size=36)

    mute = load("ui/music_on")
    surf.blit(mute, mute.get_rect(center=(WIDTH - 60, 60)))

    save(surf, "04_tangier_gameplay.png")


def capture_fez_gameplay():
    print("Capturing: Fez - Gameplay")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load("backgrounds/bg_fez")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))

    tile_back = load("items/fez_symbols/tile_back")
    symbols = ["law", "astronomy", "medicine", "theology",
               "mathematics", "philosophy", "geography", "literature"]
    random.seed(42)
    pool = symbols + symbols
    random.shuffle(pool)

    tile_w, tile_h = tile_back.get_size()
    positions = []
    for row in range(4):
        for col in range(4):
            x = 440 + col * 140
            y = 160 + row * 140
            positions.append((x, y))

    for i, (x, y) in enumerate(positions):
        if i < 4:
            sym = load(f"items/fez_symbols/symbol_{pool[i]}")
            surf.blit(sym, sym.get_rect(center=(x, y)))
        else:
            surf.blit(tile_back, tile_back.get_rect(center=(x, y)))

    back = load("ui/back_btn")
    surf.blit(back, back.get_rect(center=(80, 50)))

    draw_text(surf, "Time: 72s", (20, 100), size=36, color=(255, 255, 255))
    draw_text(surf, "Pairs: 2/8", (20, 150), size=36, color=(255, 255, 255))

    mute = load("ui/music_on")
    surf.blit(mute, mute.get_rect(center=(WIDTH - 60, 60)))

    save(surf, "05_fez_gameplay.png")


def capture_cairo_gameplay():
    print("Capturing: Cairo - Gameplay")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load("backgrounds/bg_cairo")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))

    platform = load("items/platforms/platform")
    static_pos = [(150, 650), (700, 550), (1180, 600), (300, 350), (1050, 250)]
    moving_pos = [(400, 550)]
    for pos in static_pos + moving_pos:
        surf.blit(platform, platform.get_rect(center=pos))

    cairo_items = [
        ("items/cairo/nile_water_glass", (300, 310)),
        ("items/cairo/medicine_bottle", (1050, 210)),
        ("items/collectibles/silver_dirhams", (700, 510)),
        ("items/collectibles/holy_quran", (1180, 560)),
        ("items/collectibles/oil_lamp", (450, 510)),
        ("items/collectibles/inkwell_and_kalam", (950, 410)),
        ("items/cairo/osterlab", (750, 110)),
        ("items/cairo/suger_cane", (150, 610)),
    ]
    for img_name, pos in cairo_items:
        try:
            item = load(img_name)
            surf.blit(item, item.get_rect(center=pos))
        except:
            pass

    character = load("characters/character")
    surf.blit(character, character.get_rect(center=(150, 500)))

    back = load("ui/back_btn")
    surf.blit(back, back.get_rect(center=(80, 50)))

    draw_text(surf, "Items Found: 2/8", (20, 100), size=36)

    mute = load("ui/music_on")
    surf.blit(mute, mute.get_rect(center=(WIDTH - 60, 60)))

    save(surf, "06_cairo_gameplay.png")


def capture_damascus_gameplay():
    print("Capturing: Damascus - Gameplay")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load("backgrounds/bg_damascus")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))

    back = load("ui/back_btn")
    surf.blit(back, back.get_rect(center=(80, 50)))

    character = load("characters/character")
    surf.blit(character, character.get_rect(center=(WIDTH // 2, 650)))

    falling_items = [
        ("items/collectibles/holy_quran", (400, 200)),
        ("items/collectibles/oil_lamp", (700, 350)),
        ("items/collectibles/silver_dirhams", (900, 150)),
        ("items/damascus/scorpion", (550, 450)),
        ("items/damascus/rock", (1100, 300)),
    ]
    for img_name, pos in falling_items:
        try:
            item = load(img_name)
            surf.blit(item, item.get_rect(center=pos))
        except:
            pass

    draw_text(surf, "SCORE: 12/50", (20, 100), size=44)

    mute = load("ui/music_on")
    surf.blit(mute, mute.get_rect(center=(WIDTH - 60, 60)))

    save(surf, "07_damascus_gameplay.png")


def capture_timbuktu_gameplay():
    print("Capturing: Timbuktu - Gameplay")
    surf = pygame.Surface((WIDTH, HEIGHT))
    bg = load("backgrounds/bg_timbuktu")
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    surf.blit(bg_scaled, (0, 0))

    character = load("characters/character")
    surf.blit(character, character.get_rect(center=(100, HEIGHT - 50)))

    sand = load("items/sand_particle")
    random.seed(99)
    for _ in range(25):
        sx = random.randint(0, WIDTH)
        sy = random.randint(-20, HEIGHT - 100)
        surf.blit(sand, sand.get_rect(center=(sx, sy)))

    back = load("ui/back_btn")
    surf.blit(back, back.get_rect(center=(80, 50)))

    draw_text_center(surf, "SURVIVE THE BLIZZARD: 22s", (WIDTH // 2, 100), size=48)

    mute = load("ui/music_on")
    surf.blit(mute, mute.get_rect(center=(WIDTH - 60, 60)))

    save(surf, "08_timbuktu_gameplay.png")


def main():
    print("=" * 50)
    print("  Ibn Battota - Portfolio Screenshot Capture")
    print("=" * 50)
    print()

    capture_start_screen()
    capture_world_map()

    for level, bg in [
        ("tangier", "bg_tangier"),
        ("fez", "bg_fez"),
        ("cairo", "bg_cairo"),
        ("damascus", "bg_damascus"),
        ("timbuktu", "bg_timbuktu"),
    ]:
        capture_level_with_mission(level, bg)

    capture_tangier_gameplay()
    capture_fez_gameplay()
    capture_cairo_gameplay()
    capture_damascus_gameplay()
    capture_timbuktu_gameplay()

    print()
    print("=" * 50)
    print(f"  Done! {len(os.listdir(SCREENSHOTS))} screenshots saved")
    print(f"  Location: {SCREENSHOTS}")
    print("=" * 50)

    pygame.quit()


if __name__ == "__main__":
    main()
