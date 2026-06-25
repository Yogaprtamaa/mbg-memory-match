"""Identitas visual 'Nampan Gizi' — satu sumber kebenaran palet & tipografi.

Tema MBG: kantin sekolah + poster kampanye gizi publik, dengan sisi hazard
satir untuk kartu jebakan. Dipakai oleh scene, card, dan button.
"""
import re
import pygame

# ---------- Palet (named hex) ----------
RICE_TOP = (251, 247, 236)      # latar krem nasi (atas gradient)
RICE_BOT = (236, 226, 203)      # latar krem (bawah gradient)
SPINACH = (32, 48, 42)          # tinta utama (hijau-hitam)
SPINACH_SOFT = (104, 118, 108)  # teks sekunder
TRAY = (255, 255, 255)          # permukaan kartu/panel
TRAY_LINE = (226, 215, 188)     # garis tepi halus
INK = (28, 26, 20)              # warna bayangan

LEAF = (63, 163, 77)            # hijau (gizi / aksi utama)
LEAF_DEEP = (44, 122, 59)
CARROT = (242, 135, 46)         # oranye wortel
CARROT_DEEP = (214, 108, 28)
TOMATO = (226, 67, 59)          # merah tomat (bahaya)
TOMATO_DEEP = (193, 46, 40)
GOLD = (244, 196, 48)           # emas (mark MBG / menang)
GOLD_DEEP = (212, 160, 23)
SKY = (46, 139, 192)
GRAPE = (126, 87, 194)
TEAL = (22, 166, 166)

# Warna spine per kategori (warna = informasi, bantu bedakan kategori sekilas)
SPINE = {
    "PAKET_MAKANAN": CARROT,
    "TRUK_MBG": SKY,
    "ANAK_SEKOLAH": LEAF,
    "PAK_PEMIMPIN": GRAPE,
    "PETUGAS_GIZI": TEAL,
    "OKNUM_KORUPTOR": (43, 43, 43),
    "MAKANAN_TERCEMAR": (109, 93, 75),
}


def category_color(value):
    base = re.sub(r"_\d+$", "", str(value or ""))
    return SPINE.get(base, LEAF)


# ---------- Tipografi ----------
DISPLAY = "futura"                              # judul & angka besar
BODY = "avenirnext,avenir,helveticaneue,arial"  # UI / label
MONO = "menlo,monaco,couriernew"                # data HUD (vibe label gizi)

_font_cache = {}


def font(role, size, bold=False):
    """Ambil font ber-cache. role: 'display' | 'body' | 'mono'."""
    key = (role, size, bold)
    if key not in _font_cache:
        name = {"display": DISPLAY, "body": BODY, "mono": MONO}.get(role, BODY)
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            f = pygame.font.SysFont(None, size, bold=bold)
        _font_cache[key] = f
    return _font_cache[key]
