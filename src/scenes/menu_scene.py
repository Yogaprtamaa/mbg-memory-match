import pygame
import sys
from src.scenes.scene import Scene
from src.objects.button import Button
from src.config.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, BLACK, DARK_GRAY,
    GREEN, GREEN_HOVER, RED, RED_HOVER, BLUE, BLUE_HOVER,
    ORANGE, ORANGE_HOVER, WHITE,
)


class MenuScene(Scene):
    def __init__(self, scene_manager):
        self._scene_manager = scene_manager
        self._selected_level = "EASY"

        self._title_font = pygame.font.SysFont(None, 72)
        self._subtitle_font = pygame.font.SysFont(None, 32)
        self._label_font = pygame.font.SysFont(None, 36)

        btn_w, btn_h = 200, 50
        center_x = WINDOW_WIDTH // 2 - btn_w // 2

        self._level_buttons = [
            Button(center_x - 220, 350, btn_w, btn_h, "Easy",
                   lambda: self._select_level("EASY"),
                   GREEN, GREEN_HOVER),
            Button(center_x, 350, btn_w, btn_h, "Medium",
                   lambda: self._select_level("MEDIUM"),
                   ORANGE, ORANGE_HOVER),
            Button(center_x + 220, 350, btn_w, btn_h, "Hard",
                   lambda: self._select_level("HARD"),
                   RED, RED_HOVER),
        ]

        self._play_button = Button(
            center_x, 460, btn_w, btn_h, "Play",
            self._on_play, BLUE, BLUE_HOVER,
        )

        self._quit_button = Button(
            center_x, 530, btn_w, btn_h, "Quit",
            self._on_quit, DARK_GRAY, BLACK,
        )

        self._buttons = self._level_buttons + [self._play_button, self._quit_button]

    def _select_level(self, level):
        self._selected_level = level

    def _on_play(self):
        from src.scenes.game_scene import GameScene
        scene = GameScene(self._scene_manager, self._selected_level)
        self._scene_manager.set_scene(scene)

    def _on_quit(self):
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self._buttons:
                if button.is_clicked(event.pos):
                    button.callback()

    def update(self):
        for button in self._buttons:
            button.update()

    def draw(self, screen):
        screen.fill(BG_COLOR)

        title = self._title_font.render("MBG Memory Match", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
        screen.blit(title, title_rect)

        subtitle = self._subtitle_font.render(
            "Memory Matching Game — Makan Bergizi Gratis", True, DARK_GRAY
        )
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 180))
        screen.blit(subtitle, subtitle_rect)

        label = self._label_font.render("Pilih Level:", True, BLACK)
        label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, 310))
        screen.blit(label, label_rect)

        for btn in self._level_buttons:
            btn.draw(screen)
            if btn.text.upper() == self._selected_level:
                rect = btn.get_rect()
                pygame.draw.rect(screen, WHITE, rect, 3, border_radius=8)

        self._play_button.draw(screen)
        self._quit_button.draw(screen)

        info = self._subtitle_font.render(
            f"Level: {self._selected_level}", True, DARK_GRAY
        )
        info_rect = info.get_rect(center=(WINDOW_WIDTH // 2, 620))
        screen.blit(info, info_rect)
