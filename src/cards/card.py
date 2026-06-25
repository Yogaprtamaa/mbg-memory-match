import pygame
import math
from abc import ABC, abstractmethod
from src.objects.game_object import GameObject

class Card(GameObject, ABC):
    def __init__(self, x, y, width, height, front_image_path, back_image_path):
        super().__init__()
        
        self.rect = pygame.Rect(x, y, width, height)
        self.original_width = width
        
        self.front_image = pygame.image.load(front_image_path)
        self.front_image = pygame.transform.scale(self.front_image, (width, height))
        self.back_image = pygame.image.load(back_image_path)
        self.back_image = pygame.transform.scale(self.back_image, (width, height))
        
        self.is_flipped = False
        
        
        self.is_animating = False
        self.flip_angle = 0  
        self.flip_speed = 10  
        
        try:
            self.sound_flip = pygame.mixer.Sound("assets/sounds/flip.wav")
        except pygame.error:
            self.sound_flip = None

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
                scaled_image = pygame.transform.scale(current_image, (animated_width, self.rect.height))
                new_rect = scaled_image.get_rect(center=self.rect.center)
                surface.blit(scaled_image, new_rect.topleft)
        else:
            surface.blit(current_image, self.rect.topleft)

    @abstractmethod
    def on_flip(self):
        pass