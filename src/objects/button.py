import pygame

from src.objects.game_object import GameObject
from src.utils import ui
from src.config import theme


class Button(GameObject):
    """Tombol 'pill' (kapsul penuh) bergaya design.md §6.

    Isi bisa warna solid atau gradient (mis. Play biru, peach→merah, ungu).
    Hover: naik 2px + bayangan terangkat (SHADOW_LIFT); pressed turun 1px.
    """

    def __init__(self, x, y, width, height, text, callback,
                 color=theme.BRAND_BLUE, gradient=None, hover_color=None,
                 text_color=theme.SURFACE_WHITE, font_size=22, font_role="display",
                 border_color=None):
        super().__init__(x, y, width, height)
        self.text = text
        self._callback = callback
        self._gradient = gradient            # (c1, c2) atau None
        self._color = color
        self._hover_color = hover_color or ui.lerp_color(color, (255, 255, 255), 0.14)
        self._text_color = text_color
        self._font = theme.font(font_role, font_size, bold=True)
        self._border_color = border_color
        self._hover_t = 0.0
        self._is_hovered = False

    def update(self):
        self._is_hovered = self.get_rect().collidepoint(pygame.mouse.get_pos())
        target = 1.0 if self._is_hovered else 0.0
        self._hover_t += (target - self._hover_t) * 0.25

    def _fill_surface(self, size):
        if self._gradient is not None:
            c1, c2 = self._gradient
            if self._hover_t > 0.01:
                c1 = ui.lerp_color(c1, (255, 255, 255), 0.12 * self._hover_t)
                c2 = ui.lerp_color(c2, (255, 255, 255), 0.12 * self._hover_t)
            surf = ui.horizontal_gradient(size, c1, c2)
        else:
            color = ui.lerp_color(self._color, self._hover_color, self._hover_t)
            surf = pygame.Surface(size)
            surf.fill(color)
        return surf

    def draw(self, screen):
        rect = self.get_rect()
        radius = min(rect.height // 2, theme.RADIUS_PILL)
        lift = int(2 * self._hover_t)
        center = (rect.centerx, rect.centery - lift)
        size = (rect.width, rect.height)

        ui.blit_shadow(screen, center, size, radius,
                       alpha=int(40 + 40 * self._hover_t), y_offset=6 + lift)

        rounded = ui.round_image(self._fill_surface(size), radius)
        draw_rect = rounded.get_rect(center=center)
        screen.blit(rounded, draw_rect.topleft)

        # highlight tipis di tepi atas → kesan terangkat
        hi = pygame.Rect(draw_rect.x + 6, draw_rect.y + 3,
                         draw_rect.width - 12, max(2, draw_rect.height // 2 - 4))
        glass = pygame.Surface(hi.size, pygame.SRCALPHA)
        ui.round_rect(glass, glass.get_rect(), (255, 255, 255, 46), radius)
        screen.blit(glass, hi.topleft)

        if self._border_color is not None:
            ui.round_rect(screen, draw_rect, self._border_color, radius, width=2)

        ui.text(screen, self.text, self._font, self._text_color, center=draw_rect.center)

    def is_clicked(self, pos):
        return self.get_rect().collidepoint(pos)

    def click(self):
        if self._callback is not None:
            self._callback()
