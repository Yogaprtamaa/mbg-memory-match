"""Helper gambar low-level untuk UI (gradient, shadow, rounded image, dll).

Semua fungsi murni-render; hasil yang mahal di-cache agar tetap 60 FPS.
"""
import pygame

_gradient_cache = {}
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


def soft_shadow(size, radius, alpha=70, layers=6, spread=10):
    """Bayangan lembut (rounded) di atas surface transparan, di-cache."""
    key = (size, radius, alpha, layers, spread)
    if key not in _shadow_cache:
        w, h = size
        surf = pygame.Surface((w + spread * 2, h + spread * 2), pygame.SRCALPHA)
        for i in range(layers):
            t = i / max(1, layers - 1)
            grow = int(spread * t)
            a = int(alpha * (1 - t))
            rect = pygame.Rect(spread - grow, spread - grow,
                               w + grow * 2, h + grow * 2)
            pygame.draw.rect(surf, (20, 18, 14, a), rect,
                             border_radius=radius + grow)
        _shadow_cache[key] = surf
    return _shadow_cache[key]


def blit_shadow(surface, center, size, radius, alpha=70, y_offset=8):
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


def text(surface, string, font, color, center=None, topleft=None,
         midleft=None, midright=None, shadow=None):
    surf = font.render(string, True, color)
    if shadow is not None:
        sh = font.render(string, True, shadow)
        rect = surf.get_rect()
        if center:
            rect.center = center
        elif topleft:
            rect.topleft = topleft
        elif midleft:
            rect.midleft = midleft
        elif midright:
            rect.midright = midright
        surface.blit(sh, (rect.x + 1, rect.y + 2))
        surface.blit(surf, rect)
        return rect
    rect = surf.get_rect()
    if center:
        rect.center = center
    elif topleft:
        rect.topleft = topleft
    elif midleft:
        rect.midleft = midleft
    elif midright:
        rect.midright = midright
    surface.blit(surf, rect)
    return rect
