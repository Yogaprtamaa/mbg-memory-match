import pygame

from src.objects.game_object import GameObject
from src.utils import ui
from src.config import theme


class Button(GameObject):
    """Tombol bergaya 'pill nampan': rounded, bayangan lembut, hover-lift
    dengan transisi warna halus."""

    def __init__(self, x, y, width, height, text, callback,
                 color=theme.LEAF, hover_color=None,
                 text_color=theme.TRAY, font_size=26, radius=14,
                 border_color=None):
        super().__init__(x, y, width, height)
        self.text = text
        self._callback = callback
        self._color = color
        self._hover_color = hover_color or ui.lerp_color(color, (255, 255, 255), 0.16)
        self._text_color = text_color
        self._font = theme.font("body", font_size, bold=True)
        self._radius = radius
        self._border_color = border_color
        self._hover_t = 0.0      # 0..1 animasi hover
        self._is_hovered = False

    def update(self):
        self._is_hovered = self.get_rect().collidepoint(pygame.mouse.get_pos())
        target = 1.0 if self._is_hovered else 0.0
        self._hover_t += (target - self._hover_t) * 0.25

    def draw(self, screen):
        rect = self.get_rect()
        lift = int(4 * self._hover_t)
        center = (rect.centerx, rect.centery - lift)
        size = (rect.width, rect.height)

        ui.blit_shadow(screen, center, size, self._radius,
                       alpha=int(55 + 55 * self._hover_t), y_offset=6 + lift)

        draw_rect = pygame.Rect(0, 0, *size)
        draw_rect.center = center
        color = ui.lerp_color(self._color, self._hover_color, self._hover_t)
        ui.round_rect(screen, draw_rect, color, self._radius)
        # highlight tipis di atas (depth)
        hi = pygame.Rect(draw_rect.x + 4, draw_rect.y + 3, draw_rect.width - 8, draw_rect.height // 2)
        ui.round_rect(screen, hi, ui.lerp_color(color, (255, 255, 255), 0.12), self._radius - 4)
        if self._border_color is not None:
            ui.round_rect(screen, draw_rect, self._border_color, self._radius, width=2)

        ui.text(screen, self.text, self._font, self._text_color, center=draw_rect.center)

    def is_clicked(self, pos):
        return self.get_rect().collidepoint(pos)

    def click(self):
        if self._callback is not None:
            self._callback()
