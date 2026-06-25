import sys
import math

import pygame

from src.scenes.scene import Scene
from src.objects.button import Button
from src.utils import ui
from src.config import theme
from src.config.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.config.settings import DIFFICULTY

LEVELS = ["EASY", "MEDIUM", "HARD"]
LEVEL_TINT = {"EASY": theme.LEAF, "MEDIUM": theme.CARROT, "HARD": theme.TOMATO}

CHIP_W, CHIP_H, CHIP_GAP = 220, 158, 28


class MenuScene(Scene):
    """Poster kampanye: segel MBG, judul mengambang, dan pilihan level."""

    def __init__(self, scene_manager):
        self._scene_manager = scene_manager
        self._selected_level = "EASY"
        self._t0 = pygame.time.get_ticks()

        total_w = CHIP_W * 3 + CHIP_GAP * 2
        self._chip_x0 = (WINDOW_WIDTH - total_w) // 2
        self._chip_y = 300
        self._chip_rects = {
            lvl: pygame.Rect(self._chip_x0 + i * (CHIP_W + CHIP_GAP),
                             self._chip_y, CHIP_W, CHIP_H)
            for i, lvl in enumerate(LEVELS)
        }

        self._play_button = Button(
            WINDOW_WIDTH // 2 - 140, 504, 280, 58, "Main Sekarang",
            self._on_play, theme.LEAF, font_size=28,
        )
        self._quit_button = Button(
            WINDOW_WIDTH // 2 - 80, 582, 160, 46, "Keluar",
            self._on_quit, theme.TRAY, hover_color=(244, 238, 224),
            text_color=theme.SPINACH, font_size=22, border_color=theme.TRAY_LINE,
        )

    # ---------- Aksi ----------
    def _on_play(self):
        from src.scenes.game_scene import GameScene
        self._scene_manager.set_scene(GameScene(self._scene_manager, self._selected_level))

    def _on_quit(self):
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for lvl, rect in self._chip_rects.items():
                if rect.collidepoint(event.pos):
                    self._selected_level = lvl
            for btn in (self._play_button, self._quit_button):
                if btn.is_clicked(event.pos):
                    btn.click()

    def update(self):
        self._play_button.update()
        self._quit_button.update()

    # ---------- Render ----------
    def draw(self, screen):
        screen.blit(ui.vertical_gradient(screen.get_size(), theme.RICE_TOP, theme.RICE_BOT), (0, 0))
        self._draw_header(screen)
        for lvl in LEVELS:
            self._draw_chip(screen, lvl)
        self._play_button.draw(screen)
        self._quit_button.draw(screen)
        ui.text(screen, "Cocokkan semua pasangan sebelum waktu habis — jangan buka si Koruptor.",
                theme.font("body", 19), theme.SPINACH_SOFT, center=(WINDOW_WIDTH // 2, 662))

    def _draw_header(self, screen):
        float_y = math.sin((pygame.time.get_ticks() - self._t0) * 0.002) * 4
        cx = WINDOW_WIDTH // 2

        seal = (cx, int(96 + float_y))
        pygame.draw.circle(screen, theme.GOLD, seal, 30)
        pygame.draw.circle(screen, theme.GOLD_DEEP, seal, 30, 3)
        ui.text(screen, "MBG", theme.font("display", 30, bold=True), theme.SPINACH, center=seal)

        ui.text(screen, "P R O G R A M   M A K A N   B E R G I Z I   G R A T I S",
                theme.font("body", 15, bold=True), theme.SPINACH_SOFT,
                center=(cx, int(150 + float_y)))
        ui.text(screen, "Nampan Gizi", theme.font("display", 78, bold=True),
                theme.SPINACH, center=(cx, int(200 + float_y)), shadow=theme.TRAY_LINE)

        line_w = 220
        pygame.draw.line(screen, theme.GOLD, (cx - line_w // 2, 246 + float_y),
                         (cx + line_w // 2, 246 + float_y), 3)

    def _draw_chip(self, screen, lvl):
        rect = self._chip_rects[lvl]
        cfg = DIFFICULTY[lvl]
        tint = LEVEL_TINT[lvl]
        selected = (lvl == self._selected_level)
        hover = rect.collidepoint(pygame.mouse.get_pos())

        lift = 6 if selected else (3 if hover else 0)
        draw_rect = rect.move(0, -lift)

        ui.blit_shadow(screen, draw_rect.center, rect.size, 16,
                       alpha=90 if selected else 55, y_offset=8)
        ui.round_rect(screen, draw_rect, theme.TRAY, 16)
        ui.round_rect(screen, (draw_rect.x, draw_rect.y, draw_rect.width, 8), tint, 16)
        border = tint if selected else theme.TRAY_LINE
        ui.round_rect(screen, draw_rect, border, 16, width=3 if selected else 2)

        cx = draw_rect.centerx
        ui.text(screen, lvl.title(), theme.font("display", 34, bold=True), theme.SPINACH,
                center=(cx, draw_rect.y + 46))
        ui.text(screen, f"{cfg['cols']} × {cfg['rows']} kartu", theme.font("body", 20),
                theme.SPINACH_SOFT, center=(cx, draw_rect.y + 82))
        ui.text(screen, f"{cfg['pairs']} pasang", theme.font("body", 18),
                theme.SPINACH_SOFT, center=(cx, draw_rect.y + 106))

        timer_c = (cx, draw_rect.y + 134)
        ui.text(screen, f"{cfg['time']}s", theme.font("mono", 22, bold=True),
                tint, center=timer_c)

        if selected:
            check = (draw_rect.right - 22, draw_rect.y + 26)
            pygame.draw.circle(screen, tint, check, 12)
            pygame.draw.lines(screen, theme.TRAY, False,
                              [(check[0] - 5, check[1]), (check[0] - 1, check[1] + 4),
                               (check[0] + 5, check[1] - 5)], 2)
