import pygame
<<<<<<< HEAD

class Card:
    def __init__(self, value, x, y, width, height):
        self.value = value
        self.rect = pygame.Rect(x, y, width, height)
        self.is_flipped = False
        self.is_matched = False
        
      
        from config.constants import TRAP_KORUPTOR, TRAP_TERCEMAR
        self.is_trap = value in [TRAP_KORUPTOR, TRAP_TERCEMAR]
        
       
        try:
            self.sound_flip = pygame.mixer.Sound("assets/sounds/flip.mp3")
        except pygame.error:
            self.sound_flip = None

    def flip(self):
       
        self.is_flipped = not self.is_flipped
        if self.sound_flip:
            self.sound_flip.play()

    def update(self):
        
        pass

    def draw(self, screen):
        
        if self.is_matched:
          
            return
            
        if self.is_flipped:
           
            pygame.draw.rect(screen, (230, 230, 230), self.rect, border_radius=8)
           
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
        else:
            
            pygame.draw.rect(screen, (52, 152, 219), self.rect, border_radius=8)
            pygame.draw.rect(screen, (41, 128, 185), self.rect, width=3, border_radius=8)
=======
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
            self.sound_flip = pygame.mixer.Sound("assets/sounds/flip.wav")
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
>>>>>>> c98a386 (feat: implement game architecture, scene management, and base card logic with trap support and finish fitur 1 and 2)
