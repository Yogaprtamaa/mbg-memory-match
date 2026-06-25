import math
import re
from abc import ABC, abstractmethod

import pygame

from src.objects.game_object import GameObject
from src.utils.asset_loader import get_asset_loader
from src.utils import ui
from src.config import theme
from src.config.settings import SOUND_PATH

FLIP_SOUND = SOUND_PATH + "flip.mp3"
CARD_RADIUS = 14
PAD = 9
SPINE_H = 14


class Card(GameObject, ABC):
    """Kartu 'ubin nampan': bingkai putih, foto membulat, spine kategori,
    punggung kupon bersegel emas.

    State (flip/matched/animasi/hover) private; hanya diubah lewat method
    dan diakses via property read-only — bukti Encapsulation.
    """

    def __init__(self, x, y, width, height, value,
                 front_image_path=None, back_image_path=None,
                 front_color=(76, 175, 80)):
        super().__init__(x, y, width, height)
        self._value = value
        self._rect = pygame.Rect(x, y, width, height)
        self._face_size = (width, height)
        self._spine = theme.category_color(value)

        loader = get_asset_loader()
        match = re.search(r"_(\d+)$", str(value)) if value else None
        badge = match.group(1) if match else None
        raw_front = loader.load_image(
            front_image_path, (width, height), front_color, value or "", badge
        )
        self._front_face = self._build_front_face(raw_front)
        self._back_face = self._build_back_face()
        self._sound_flip = loader.load_sound(FLIP_SOUND)

        self._is_flipped = False
        self._is_matched = False
        self._is_animating = False
        self._hover = False
        self._flip_angle = 0
        self._flip_speed = 10

    # ---------- Komposisi tampilan ----------
    def _build_front_face(self, raw_front):
        w, h = self._face_size
        face = pygame.Surface((w, h), pygame.SRCALPHA)
        ui.round_rect(face, (0, 0, w, h), theme.TRAY, CARD_RADIUS)

        img_w = w - PAD * 2
        img_h = h - PAD * 2 - SPINE_H - 4
        photo = ui.round_image(pygame.transform.smoothscale(raw_front, (img_w, img_h)), 8)
        face.blit(photo, (PAD, PAD))

        spine = pygame.Rect(PAD, h - PAD - SPINE_H, w - PAD * 2, SPINE_H)
        ui.round_rect(face, spine, self._spine, 7)
        ui.round_rect(face, (0, 0, w, h), theme.TRAY_LINE, CARD_RADIUS, width=2)
        return face

    def _build_back_face(self):
        w, h = self._face_size
        back = pygame.Surface((w, h), pygame.SRCALPHA)
        ui.round_rect(back, (0, 0, w, h), theme.SPINACH, CARD_RADIUS)
        ui.round_rect(back, (6, 6, w - 12, h - 12), (26, 40, 34), CARD_RADIUS - 3)
        ui.round_rect(back, (6, 6, w - 12, h - 12), theme.GOLD_DEEP, CARD_RADIUS - 3, width=1)

        seal = (w // 2, h // 2 - 6)
        pygame.draw.circle(back, theme.GOLD, seal, 22)
        pygame.draw.circle(back, theme.GOLD_DEEP, seal, 22, 3)
        ui.text(back, "MBG", theme.font("display", 24, bold=True), theme.SPINACH, center=seal)
        ui.text(back, "NAMPAN GIZI", theme.font("body", 13), theme.GOLD,
                center=(w // 2, h // 2 + 28))
        return back

    # ---------- Property read-only ----------
    @property
    def value(self):
        return self._value

    @property
    def rect(self):
        return self._rect

    @property
    def is_flipped(self):
        return self._is_flipped

    @property
    def is_matched(self):
        return self._is_matched

    @property
    def is_animating(self):
        return self._is_animating

    # ---------- Perilaku ----------
    def flip(self):
        if not self._is_animating:
            self._is_animating = True
            if self._sound_flip is not None:
                self._sound_flip.play()

    def mark_matched(self):
        self._is_matched = True

    def set_hover(self, value):
        self._hover = bool(value)

    def update(self):
        if not self._is_animating:
            return
        self._flip_angle += self._flip_speed
        if self._flip_angle >= 90 and self._flip_angle - self._flip_speed < 90:
            self._is_flipped = not self._is_flipped
        if self._flip_angle >= 180:
            self._flip_angle = 0
            self._is_animating = False

    def draw(self, surface):
        face = self._front_face if self._is_flipped else self._back_face
        w, h = self._face_size
        cx, cy = self._rect.center
        lift = -6 if (self._hover and not self._is_matched and not self._is_animating) else 0
        center = (cx, cy + lift)

        if self._is_matched:
            pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.005)
            glow = pygame.Surface((w + 26, h + 26), pygame.SRCALPHA)
            ui.round_rect(glow, glow.get_rect(), (*theme.LEAF, int(55 + 70 * pulse)), 20)
            surface.blit(glow, glow.get_rect(center=center).topleft)

        ui.blit_shadow(surface, center, self._face_size, CARD_RADIUS,
                       alpha=95 if lift else 65, y_offset=8 - lift)

        if self._is_animating:
            scale_factor = abs(math.cos(math.radians(self._flip_angle)))
            animated_width = max(1, int(w * scale_factor))
            scaled = pygame.transform.scale(face, (animated_width, h))
            surface.blit(scaled, scaled.get_rect(center=center).topleft)
        else:
            surface.blit(face, face.get_rect(center=center).topleft)

    @abstractmethod
    def on_flip(self):
        """Polymorphic: kembalikan FlipResult sesuai jenis kartu."""
        pass
