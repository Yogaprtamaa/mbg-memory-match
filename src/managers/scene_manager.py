import pygame

from src.config import theme


class SceneManager:
    """Mengelola scene aktif + transisi fade-in ringan saat pindah scene."""

    def __init__(self):
        self._current = None
        self._fade_alpha = 0
        self._overlay = None

    def set_scene(self, scene):
        self._current = scene
        self._fade_alpha = 255  # mulai dari tertutup, lalu memudar

    def handle_event(self, event):
        if self._current:
            self._current.handle_event(event)

    def update(self):
        if self._current:
            self._current.update()

    def draw(self, screen):
        if not self._current:
            return
        self._current.draw(screen)
        if self._fade_alpha > 0:
            if self._overlay is None or self._overlay.get_size() != screen.get_size():
                self._overlay = pygame.Surface(screen.get_size())
                self._overlay.fill(theme.BG_CREAM)
            self._overlay.set_alpha(self._fade_alpha)
            screen.blit(self._overlay, (0, 0))
            self._fade_alpha = max(0, self._fade_alpha - 22)
