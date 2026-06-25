import pygame
from src.objects.game_object import GameObject


class Button(GameObject):
    def __init__(self, x, y, width, height, text, callback,
                 color=(76, 175, 80), hover_color=(56, 142, 60),
                 text_color=(255, 255, 255), font_size=28):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self._is_hovered = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self._is_hovered = self.get_rect().collidepoint(mouse_pos)

    def draw(self, screen):
        current_color = self.hover_color if self._is_hovered else self.color
        rect = self.get_rect()
        pygame.draw.rect(screen, current_color, rect, border_radius=8)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.get_rect().collidepoint(pos)
