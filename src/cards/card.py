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
RADIUS = theme.RADIUS_CARD
PAD = 9
SPINE_H = 12
EDGE_DROP = 4  # offset "tebal" kartu → kesan 3D (design.md §3a)

# Pasangan tint/edge muka belakang (papan catur posisi, bukan nilai kartu).
BACK_TINTS = {
    "peach": (theme.CARD_PEACH, theme.CARD_PEACH_EDGE),
    "lavender": (theme.CARD_LAVENDER, theme.CARD_LAV_EDGE),
}


class Card(GameObject, ABC):
    """Kartu 3D membulat (design.md §3): belakang peach/lavender beremboss MBG,
    depan putih dengan gambar MBG + spine kategori.

    State (flip/matched/animasi/hover) private; hanya diubah lewat method
    dan diakses via property read-only — bukti Encapsulation.
    """

    def __init__(self, x, y, width, height, value,
                 front_image_path=None, back_image_path=None,
                 front_color=theme.CARD_PEACH):
        super().__init__(x, y, width, height)
        self._value = value
        self._rect = pygame.Rect(x, y, width, height)
        self._face_size = (width, height)
        self._spine = theme.category_color(value)
        self._back_kind = "peach"

        loader = get_asset_loader()
        match = re.search(r"_(\d+)$", str(value)) if value else None
        badge = match.group(1) if match else None
        raw_front = loader.load_image(
            front_image_path, (width, height), front_color, value or "", badge
        )
        self._front_face = self._build_front_face(raw_front)
        self._back_face = self._build_back_face("peach")
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
        ui.round_rect(face, (0, 0, w, h), theme.SURFACE_WHITE, RADIUS)

        img_w = w - PAD * 2
        img_h = h - PAD * 2 - SPINE_H - 4
        photo = ui.round_image(pygame.transform.smoothscale(raw_front, (img_w, img_h)), 12)
        face.blit(photo, (PAD, PAD))

        spine = pygame.Rect(PAD, h - PAD - SPINE_H, w - PAD * 2, SPINE_H)
        ui.round_rect(face, spine, self._spine, SPINE_H // 2)
        ui.round_rect(face, (0, 0, w, h), theme.HAIRLINE, RADIUS, width=2)
        return face

    def _build_back_face(self, kind):
        w, h = self._face_size
        base, _ = BACK_TINTS.get(kind, BACK_TINTS["peach"])
        top = ui.lerp_color(base, (255, 255, 255), 0.22)
        grad = ui.vertical_gradient((w, h), top, base)
        back = ui.round_image(grad, RADIUS)

        # highlight tepi atas + bayangan tepi bawah-dalam → volume
        ui.round_rect(back, (2, 2, w - 4, h - 4),
                      ui.lerp_color(base, (255, 255, 255), 0.45), RADIUS - 2, width=2)

        # ikon emboss MBG di tengah (dua bayangan: gelap lalu terang)
        cx, cy = w // 2, h // 2
        r = max(16, min(w, h) // 4)
        dark = ui.lerp_color(base, (0, 0, 0), 0.18)
        light = ui.lerp_color(base, (255, 255, 255), 0.55)
        pygame.draw.circle(back, dark, (cx, cy + 1), r)
        pygame.draw.circle(back, light, (cx, cy - 1), r)
        pygame.draw.circle(back, base, (cx, cy), r)
        pygame.draw.circle(back, ui.lerp_color(base, (255, 255, 255), 0.6), (cx, cy), r, 2)
        f = theme.font("display", max(16, r), bold=True)
        ui.text(back, "MBG", f, dark, center=(cx, cy + 1))
        ui.text(back, "MBG", f, light, center=(cx, cy))
        return back

    def set_back_tint(self, kind):
        """Set tint belakang (papan catur: 'peach'/'lavender'). Bangun ulang muka."""
        if kind != self._back_kind:
            self._back_kind = kind
            self._back_face = self._build_back_face(kind)

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
            ui.round_rect(glow, glow.get_rect(),
                          (*theme.SUCCESS_GREEN, int(50 + 70 * pulse)), RADIUS + 4)
            surface.blit(glow, glow.get_rect(center=center).topleft)

        ui.blit_shadow(surface, center, self._face_size, RADIUS,
                       alpha=70 if lift else 46, y_offset=10 - lift)

        if self._is_animating:
            scale_factor = abs(math.cos(math.radians(self._flip_angle)))
            animated_width = max(1, int(w * scale_factor))
            scaled = pygame.transform.scale(face, (animated_width, h))
            surface.blit(scaled, scaled.get_rect(center=center).topleft)
        else:
            # "tebal" kartu: rect lebih gelap di-offset ke bawah → 3D
            if self._is_flipped:
                edge = theme.WHITE_EDGE
            else:
                edge = BACK_TINTS.get(self._back_kind, BACK_TINTS["peach"])[1]
            edge_rect = pygame.Rect(center[0] - w // 2, center[1] - h // 2 + EDGE_DROP, w, h)
            ui.round_rect(surface, edge_rect, edge, RADIUS)
            surface.blit(face, face.get_rect(center=center).topleft)

    @abstractmethod
    def on_flip(self):
        """Polymorphic: kembalikan FlipResult sesuai jenis kartu."""
        pass
