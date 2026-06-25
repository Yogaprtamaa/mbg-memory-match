import pygame
import math
import os
from abc import ABC, abstractmethod
from src.objects.game_object import GameObject
from src.config.constants import CARD_BACK_COLOR, WHITE


class Card(GameObject, ABC):

    def __init__(self, x, y, width, height, value,
                 front_image_path=None, back_image_path=None,
                 front_color=(76, 175, 80)):
        super().__init__(x, y, width, height)
        self.value = value
        self.is_matched = False
        self.rect = pygame.Rect(x, y, width, height)
        self.original_width = width

        self.front_image = self._load_image(
            front_image_path, width, height, front_color, value
        )
        self.back_image = self._load_image(
            back_image_path, width, height, CARD_BACK_COLOR, "?"
        )

        self.is_flipped = False
        self.is_animating = False
        self.flip_angle = 0
        self.flip_speed = 10

        try:
            self.sound_flip = pygame.mixer.Sound("assets/sounds/flip.mp3")
        except (pygame.error, FileNotFoundError):
            self.sound_flip = None

    @staticmethod
    def _load_image(path, width, height, fallback_color, label):
        if path and os.path.exists(path):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, (width, height))

        surface = pygame.Surface((width, height))
        surface.fill(fallback_color)
        pygame.draw.rect(surface, WHITE, surface.get_rect(), 3, border_radius=6)

        display = label.replace("_", " ")
        font = pygame.font.SysFont(None, 20)
        words = display.split()
        lines = []
        current = ""
        for w in words:
            test = f"{current} {w}".strip()
            if font.size(test)[0] <= width - 16:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)

        total_h = len(lines) * 22
        start_y = (height - total_h) // 2
        for i, line in enumerate(lines):
            text = font.render(line, True, WHITE)
            rect = text.get_rect(center=(width // 2, start_y + i * 22 + 11))
            surface.blit(text, rect)
        return surface

    def flip(self):
        if not self.is_animating:
            self.is_animating = True
            if self.sound_flip:
                self.sound_flip.play()

    def update(self):
        if self.is_animating:
            self.flip_angle += self.flip_speed
            if self.flip_angle >= 90 and self.flip_angle - self.flip_speed < 90:
                self.is_flipped = not self.is_flipped
            if self.flip_angle >= 180:
                self.flip_angle = 0
                self.is_animating = False

    def draw(self, surface):
        current_image = self.front_image if self.is_flipped else self.back_image

        if self.is_animating:
            scale_factor = abs(math.cos(math.radians(self.flip_angle)))
            animated_width = int(self.original_width * scale_factor)
            if animated_width > 0:
                scaled = pygame.transform.scale(
                    current_image, (animated_width, self.rect.height)
                )
                new_rect = scaled.get_rect(center=self.rect.center)
                surface.blit(scaled, new_rect.topleft)
        else:
            surface.blit(current_image, self.rect.topleft)

    @abstractmethod
    def on_flip(self):
        pass
