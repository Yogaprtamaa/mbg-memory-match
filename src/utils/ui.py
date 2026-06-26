"""Helper gambar low-level untuk UI (gradient, shadow, kaca, teks gradien).

Look pastel-glass (docs/design.md §6) "dibikin tangan". Semua fungsi murni-render;
hasil mahal di-cache agar tetap 60 FPS — pra-render yang statis, jangan tiap frame.
"""
import numpy as np
import pygame

from src.config import theme

_gradient_cache = {}
_hgradient_cache = {}
_diag_cache = {}
_shadow_cache = {}


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def vertical_gradient(size, top_color, bottom_color):
    """Surface gradient vertikal (di-cache per parameter)."""
    key = (size, top_color, bottom_color)
    if key not in _gradient_cache:
        width, height = size
        surf = pygame.Surface(size)
        for y in range(height):
            t = y / max(1, height - 1)
            pygame.draw.line(surf, lerp_color(top_color, bottom_color, t),
                             (0, y), (width, y))
        _gradient_cache[key] = surf
    return _gradient_cache[key]


def horizontal_gradient(size, left_color, right_color):
    """Surface gradient horizontal (di-cache per parameter)."""
    key = (size, left_color, right_color)
    if key not in _hgradient_cache:
        width, height = size
        surf = pygame.Surface(size)
        for x in range(width):
            t = x / max(1, width - 1)
            pygame.draw.line(surf, lerp_color(left_color, right_color, t),
                             (x, 0), (x, height))
        _hgradient_cache[key] = surf
    return _hgradient_cache[key]


def four_stop_diagonal(size, stops):
    """Latar gradient 4-stop diagonal (kiri-atas → kanan-bawah), di-cache.

    Dihitung sekali di resolusi kecil lalu di-`smoothscale` ke ukuran window
    (cepat & mulus) — sesuai aturan performa design.md (jangan tiap frame).
    """
    key = (size, tuple(stops))
    if key not in _diag_cache:
        w, h = size
        sw, sh = max(2, w // 4), max(2, h // 4)
        xs = np.linspace(0.0, 1.0, sw)[None, :]
        ys = np.linspace(0.0, 1.0, sh)[:, None]
        t = (xs + ys) * 0.5                      # parameter diagonal 0..1
        n = len(stops) - 1
        seg = np.clip(t * n, 0, n)
        idx = np.clip(seg.astype(int), 0, n - 1)
        frac = (seg - idx)[..., None]
        cols = np.array(stops, dtype=float)
        arr = cols[idx] + (cols[idx + 1] - cols[idx]) * frac  # (sh, sw, 3)
        small = pygame.surfarray.make_surface(
            np.ascontiguousarray(arr.transpose(1, 0, 2).astype(np.uint8)))
        _diag_cache[key] = pygame.transform.smoothscale(small, (w, h))
    return _diag_cache[key]


def background(size):
    """Latar baku semua scene: gradient diagonal 4-stop pastel."""
    return four_stop_diagonal(size, theme.BG_STOPS)


def soft_shadow(size, radius, alpha=46, layers=6, spread=12, color=theme.SHADOW):
    """Bayangan lembut (rounded) di atas surface transparan, di-cache."""
    key = (size, radius, alpha, layers, spread, color)
    if key not in _shadow_cache:
        w, h = size
        surf = pygame.Surface((w + spread * 2, h + spread * 2), pygame.SRCALPHA)
        for i in range(layers):
            t = i / max(1, layers - 1)
            grow = int(spread * t)
            a = int(alpha * (1 - t))
            rect = pygame.Rect(spread - grow, spread - grow,
                               w + grow * 2, h + grow * 2)
            pygame.draw.rect(surf, (*color, a), rect, border_radius=radius + grow)
        _shadow_cache[key] = surf
    return _shadow_cache[key]


def blit_shadow(surface, center, size, radius, alpha=46, y_offset=8):
    shadow = soft_shadow(size, radius, alpha)
    rect = shadow.get_rect(center=(center[0], center[1] + y_offset))
    surface.blit(shadow, rect.topleft)


def round_image(image, radius):
    """Kembalikan salinan image dengan sudut membulat (alpha mask)."""
    size = image.get_size()
    result = image.convert_alpha()
    mask = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
    result.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return result


def round_rect(surface, rect, color, radius, width=0):
    pygame.draw.rect(surface, color, rect, width, border_radius=radius)


def star(surface, center, radius, color, points=5):
    """Bintang isi (vektor) — aman tanpa font emoji."""
    import math
    cx, cy = center
    verts = []
    for i in range(points * 2):
        r = radius if i % 2 == 0 else radius * 0.44
        a = -math.pi / 2 + i * math.pi / points
        verts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pygame.draw.polygon(surface, color, verts)


def glass_panel(surface, rect, radius=theme.RADIUS_PANEL, alpha=150):
    """Panel kaca (glassmorphism): bayangan + isi putih translusen + tepi terang.

    Pendekatan praktis design.md §6 — putih semi-transparan di atas latar pastel
    sudah membaca sebagai 'kaca' tanpa blur per frame.
    """
    blit_shadow(surface, rect.center, rect.size, radius, alpha=42, y_offset=10)
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    local = panel.get_rect()
    round_rect(panel, local, (255, 255, 255, alpha), radius)
    round_rect(panel, local, theme.GLASS_BORDER, radius, width=2)
    surface.blit(panel, rect.topleft)


def gradient_text_surface(string, font, c1, c2):
    """Teks dengan isian gradient horizontal c1→c2 (alpha dari teks)."""
    ts = font.render(string, True, (255, 255, 255)).convert_alpha()
    tw, th = ts.get_size()
    if tw == 0 or th == 0:
        return ts
    grad = horizontal_gradient((tw, th), c1, c2).convert_alpha()
    grad.blit(ts, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return grad


def gradient_text(surface, string, font, c1, c2, center=None, topleft=None,
                  midleft=None, shadow=None):
    surf = gradient_text_surface(string, font, c1, c2)
    rect = surf.get_rect()
    if center:
        rect.center = center
    elif topleft:
        rect.topleft = topleft
    elif midleft:
        rect.midleft = midleft
    if shadow is not None:
        sh = font.render(string, True, shadow)
        surface.blit(sh, (rect.x + 1, rect.y + 2))
    surface.blit(surf, rect)
    return rect


def text(surface, string, font, color, center=None, topleft=None,
         midleft=None, midright=None, shadow=None):
    surf = font.render(string, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = center
    elif topleft:
        rect.topleft = topleft
    elif midleft:
        rect.midleft = midleft
    elif midright:
        rect.midright = midright
    if shadow is not None:
        sh = font.render(string, True, shadow)
        surface.blit(sh, (rect.x + 1, rect.y + 2))
    surface.blit(surf, rect)
    return rect
