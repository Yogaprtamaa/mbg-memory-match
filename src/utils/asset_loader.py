import os
import pygame

from src.config.constants import (
    WHITE, BADGE_BG_COLOR, BADGE_TEXT_COLOR, BADGE_RADIUS,
)


class AssetLoader:
    """Pemuat aset terpusat dengan cache + fallback aman.

    Menghindari anti-pattern memuat ulang aset yang sama berkali-kali
    (mis. sound flip yang sebelumnya di-load per kartu). Gambar di-cache
    per (path, ukuran); sound di-cache per path. Bila file tidak ada,
    gambar jatuh ke surface fallback (warna + label), sound jadi None.
    """

    _FALLBACK_FONT_SIZE = 20
    _LINE_HEIGHT = 22

    def __init__(self):
        self._images = {}
        self._sounds = {}

    # ---------- Gambar ----------
    def load_image(self, path, size=None, fallback_color=(76, 175, 80),
                   label="", badge=None):
        key = (path, size, badge)
        if key not in self._images:
            surface = self._create_image(path, size, fallback_color, label)
            if badge:
                self._stamp_badge(surface, str(badge))
            self._images[key] = surface
        return self._images[key]

    @classmethod
    def _stamp_badge(cls, surface, text):
        # _create_image selalu menghasilkan Surface baru, jadi aman di-stamp
        # langsung tanpa merusak entri cache lain (key mengandung badge).
        cx = surface.get_width() - BADGE_RADIUS - 4
        cy = BADGE_RADIUS + 4
        pygame.draw.circle(surface, BADGE_BG_COLOR, (cx, cy), BADGE_RADIUS)
        pygame.draw.circle(surface, WHITE, (cx, cy), BADGE_RADIUS, 2)
        font = pygame.font.SysFont(None, BADGE_RADIUS * 2)
        rendered = font.render(text, True, BADGE_TEXT_COLOR)
        surface.blit(rendered, rendered.get_rect(center=(cx, cy)))

    def _create_image(self, path, size, fallback_color, label):
        if path and os.path.exists(path):
            try:
                image = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(image, size) if size else image
            except pygame.error:
                pass
        return self._build_fallback(size or (100, 140), fallback_color, label)

    @classmethod
    def _build_fallback(cls, size, color, label):
        width, height = size
        surface = pygame.Surface(size)
        surface.fill(color)
        pygame.draw.rect(surface, WHITE, surface.get_rect(), 3, border_radius=6)

        text = (label or "").replace("_", " ").strip()
        if not text:
            return surface

        font = pygame.font.SysFont(None, cls._FALLBACK_FONT_SIZE)
        lines = cls._wrap_text(text, font, width - 16)
        total_h = len(lines) * cls._LINE_HEIGHT
        start_y = (height - total_h) // 2
        for i, line in enumerate(lines):
            rendered = font.render(line, True, WHITE)
            rect = rendered.get_rect(
                center=(width // 2, start_y + i * cls._LINE_HEIGHT + cls._LINE_HEIGHT // 2)
            )
            surface.blit(rendered, rect)
        return surface

    @staticmethod
    def _wrap_text(text, font, max_width):
        lines, current = [], ""
        for word in text.split():
            candidate = f"{current} {word}".strip()
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    # ---------- Sound ----------
    def load_sound(self, path):
        if path not in self._sounds:
            sound = None
            if path and os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                except pygame.error:
                    sound = None
            self._sounds[path] = sound
        return self._sounds[path]

    def play_sound(self, path):
        sound = self.load_sound(path)
        if sound is not None:
            sound.play()


_loader = None


def get_asset_loader():
    """Akses singleton AssetLoader (lazy; aman dipanggil setelah pygame.init)."""
    global _loader
    if _loader is None:
        _loader = AssetLoader()
    return _loader
