"""Identitas visual 'MBG Memory Match' — satu sumber kebenaran token.

Arah desain (lihat docs/design.md): soft pastel playful + kartu 3D membulat +
panel kaca (glassmorphism), latar gradient diagonal 4-stop. Dipakai oleh scene,
card, dan button. Komponen TIDAK boleh memakai hex liar di luar token ini.
"""
import os
import re
import pygame

from src.config.settings import FONT_PATH

# ---------- Palet (design.md §1a) ----------
# Latar: gradient diagonal cream → rose → lavender → sky (kiri-atas → kanan-bawah).
BG_STOPS = [(251, 244, 234), (247, 232, 236), (233, 224, 246), (220, 234, 246)]
BG_CREAM, BG_ROSE, BG_LAVENDER, BG_SKY = BG_STOPS

BRAND_BLUE = (110, 143, 230)     # awal gradient logo/judul
BRAND_PURPLE = (154, 111, 224)   # akhir gradient logo/judul, aksen ungu

CARD_PEACH = (244, 169, 125)     # muka belakang kartu (tint A)
CARD_PEACH_EDGE = (228, 142, 92) # sisi/tebal kartu peach (efek 3D)
CARD_LAVENDER = (197, 176, 232)  # muka belakang kartu (tint B)
CARD_LAV_EDGE = (171, 144, 218)  # sisi/tebal kartu lavender

SURFACE_WHITE = (255, 255, 255)  # kartu menu solid, muka kartu terbuka
HAIRLINE = (233, 224, 238)       # garis tepi halus (pengganti hitam)
WHITE_EDGE = (226, 219, 232)     # "tebal" 3D kartu putih (muka depan)

GLASS_FILL = (255, 255, 255, 150)    # isi panel kaca HUD
GLASS_BORDER = (255, 255, 255, 200)  # garis tepi-highlight panel kaca

SUCCESS_GREEN = (111, 191, 115)  # kartu cocok, badge "sehat", progress
SUCCESS_GLOW = (166, 224, 168)   # glow saat match
SCORE_GOLD = (246, 196, 90)      # ikon bintang skor / segel menang
SCORE_GOLD_DEEP = (224, 168, 56)
DANGER_RED = (229, 101, 78)      # KORUPTOR, layar kalah, vignette
TERCEMAR_OLIVE = (169, 162, 62)  # flash kartu makanan tercemar

INK = (110, 90, 107)             # teks utama (plum keabu hangat)
INK_MUTED = (154, 140, 163)      # teks sekunder, caption, label
SHADOW = (110, 90, 107)          # warna drop shadow lembut (alpha diatur di ui)

# ---------- Bentuk & spasi (design.md §1c) ----------
RADIUS_CARD = 20
RADIUS_PANEL = 28
RADIUS_PILL = 999
RADIUS_SM = 12
GAP_CARD = 16
SPACE = (4, 8, 12, 16, 24, 32, 48)

# Aksen pastel per kategori (warna = informasi, bantu bedakan saat kartu terbuka)
SPINE = {
    "PAKET_MAKANAN": CARD_PEACH,
    "TRUK_MBG": BRAND_BLUE,
    "ANAK_SEKOLAH": SUCCESS_GREEN,
    "PAK_PEMIMPIN": BRAND_PURPLE,
    "PETUGAS_GIZI": (96, 196, 196),
    "OKNUM_KORUPTOR": (96, 84, 96),
    "MAKANAN_TERCEMAR": TERCEMAR_OLIVE,
}


def category_color(value):
    base = re.sub(r"_\d+$", "", str(value or ""))
    return SPINE.get(base, BRAND_PURPLE)


# ---------- Tipografi (design.md §1b) ----------
# Pasangan rounded: Display = Fredoka, Body/Data = Nunito. Jika file font tidak
# ada di assets/fonts/, jatuh ke SysFont rounded — game tetap jalan (PRD §8).
_FONT_FILES = {
    "display": "Fredoka-SemiBold.ttf",
    "body": "Nunito-Regular.ttf",
    "data": "Nunito-ExtraBold.ttf",
}
# Daftar fallback: utamakan font rounded yang lazim ada di sistem.
_FALLBACK = "fredoka,baloo2,quicksand,arialroundedmtbold,avenirnext,helveticaneue,arial"
_ALWAYS_BOLD = {"display", "data"}

_font_cache = {}


def font(role, size, bold=False):
    """Ambil font ber-cache. role: 'display' | 'body' | 'data'."""
    key = (role, size, bold)
    if key not in _font_cache:
        path = os.path.join(FONT_PATH, _FONT_FILES.get(role, _FONT_FILES["body"]))
        f = None
        if os.path.exists(path):
            try:
                f = pygame.font.Font(path, size)
                f.set_bold(bold)
            except Exception:
                f = None
        if f is None:
            want_bold = bold or role in _ALWAYS_BOLD
            try:
                f = pygame.font.SysFont(_FALLBACK, size, bold=want_bold)
            except Exception:
                f = pygame.font.SysFont(None, size, bold=want_bold)
        _font_cache[key] = f
    return _font_cache[key]
