<<<<<<< HEAD
import pygame

# Window Configurations
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# Colors
COLOR_BG = (240, 248, 255)       # Alice Blue
COLOR_PRIMARY = (30, 144, 255)   # Dodger Blue
COLOR_SECONDARY = (70, 130, 180) # Steel Blue
COLOR_TEXT = (44, 62, 80)
COLOR_CARD_BACK = (52, 152, 219)
COLOR_WHITE = (255, 255, 255)

# Card Value Identifiers (Enum-like)
CARD_VALUES = [
    "PAKET_MAKANAN_1", "PAKET_MAKANAN_2", 
    "TRUK_MBG_1", "TRUK_MBG_2",
    "ANAK_SEKOLAH_1", "ANAK_SEKOLAH_2",
    "PAK_PEMIMPIN_1", "PAK_PEMIMPIN_2",
    "PETUGAS_GIZI_1", "PETUGAS_GIZI_2",
    "VARIAN_EXTRA_1"
]

TRAP_KORUPTOR = "OKNUM_KORUPTOR"
TRAP_TERCEMAR = "MAKANAN_TERCEMAR"

# Difficulty Enums
LEVEL_EASY = "EASY"
LEVEL_MEDIUM = "MEDIUM"
LEVEL_HARD = "HARD"
=======
# Window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60
GAME_TITLE = "MBG Memory Match"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (76, 175, 80)
GREEN_HOVER = (56, 142, 60)
RED = (244, 67, 54)
RED_HOVER = (211, 47, 47)
BLUE = (33, 150, 243)
BLUE_HOVER = (25, 118, 210)
ORANGE = (255, 152, 0)
ORANGE_HOVER = (245, 124, 0)
BG_COLOR = (245, 245, 220)

# Card categories
PAKET_MAKANAN = "PAKET_MAKANAN"
TRUK_MBG = "TRUK_MBG"
ANAK_SEKOLAH = "ANAK_SEKOLAH"
PAK_PEMIMPIN = "PAK_PEMIMPIN"
PETUGAS_GIZI = "PETUGAS_GIZI"

# Trap values
OKNUM_KORUPTOR = "OKNUM_KORUPTOR"
MAKANAN_TERCEMAR = "MAKANAN_TERCEMAR"

# 11 unique match values (enough for Hard mode)
MATCH_VALUES = [
    "PAKET_MAKANAN_1",
    "PAKET_MAKANAN_2",
    "PAKET_MAKANAN_3",
    "TRUK_MBG_1",
    "TRUK_MBG_2",
    "ANAK_SEKOLAH_1",
    "ANAK_SEKOLAH_2",
    "PAK_PEMIMPIN_1",
    "PAK_PEMIMPIN_2",
    "PETUGAS_GIZI_1",
    "PETUGAS_GIZI_2",
]

# Fallback colors per index (for cards without image assets)
CARD_FRONT_COLORS = [
    (76, 175, 80),
    (56, 142, 60),
    (129, 199, 132),
    (33, 150, 243),
    (25, 118, 210),
    (255, 193, 7),
    (255, 152, 0),
    (244, 67, 54),
    (233, 30, 99),
    (156, 39, 176),
    (0, 188, 212),
]

TRAP_COLORS = {
    OKNUM_KORUPTOR: (183, 28, 28),
    MAKANAN_TERCEMAR: (62, 39, 35),
}

CARD_BACK_COLOR = (55, 71, 79)

# Card dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 140
CARD_MARGIN = 15

# HUD
HUD_HEIGHT = 60

# Scoring
SCORE_MATCH = 10
SCORE_MISMATCH = -2
SCORE_TRAP_PENALTY = -10
TIMER_TRAP_PENALTY = 15
BONUS_MULTIPLIER = 2

# Timing (ms)
MISMATCH_DELAY = 800
>>>>>>> c98a386 (feat: implement game architecture, scene management, and base card logic with trap support and finish fitur 1 and 2)
