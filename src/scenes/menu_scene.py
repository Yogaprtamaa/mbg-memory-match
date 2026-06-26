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
LEVEL_LABEL = {"EASY": "Easy", "MEDIUM": "Medium", "HARD": "Hard"}
LEVEL_STARS = {"EASY": 1, "MEDIUM": 2, "HARD": 3}
# Gradient pill Play per level (design.md §2a): Easy biru, Medium peach→merah, Hard ungu.
LEVEL_GRAD = {
    "EASY": (theme.BRAND_BLUE, (130, 170, 235)),
    "MEDIUM": (theme.CARD_PEACH, theme.DANGER_RED),
    "HARD": (theme.BRAND_PURPLE, (190, 150, 235)),
}
LEVEL_ACCENT = {"EASY": theme.BRAND_BLUE, "MEDIUM": theme.DANGER_RED, "HARD": theme.BRAND_PURPLE}

CARD_W, CARD_H, CARD_GAP = 248, 320, 28
RAISE = 22  # kartu Medium "POPULER" sedikit terangkat


class MenuScene(Scene):
    """Soft-pastel hero: judul gradient + tiga kartu level (design.md §2a)."""

    def __init__(self, scene_manager):
        self._scene_manager = scene_manager
        self._t0 = pygame.time.get_ticks()

        total_w = CARD_W * 3 + CARD_GAP * 2
        x0 = (WINDOW_WIDTH - total_w) // 2
        base_y = 286
        self._card_rects = {}
        self._play_buttons = {}
        for i, lvl in enumerate(LEVELS):
            raise_y = RAISE if lvl == "MEDIUM" else 0
            rect = pygame.Rect(x0 + i * (CARD_W + CARD_GAP), base_y - raise_y, CARD_W, CARD_H)
            self._card_rects[lvl] = rect
            self._play_buttons[lvl] = Button(
                rect.centerx - 88, rect.bottom - 70, 176, 50, "Main",
                self._make_play(lvl), gradient=LEVEL_GRAD[lvl], font_size=22,
            )

        self._quit_button = Button(
            WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT - 56, 140, 40, "Keluar",
            self._on_quit, color=theme.SURFACE_WHITE,
            text_color=theme.INK_MUTED, font_size=16, border_color=theme.HAIRLINE,
        )

    # ---------- Aksi ----------
    def _make_play(self, level):
        def _play():
            from src.scenes.game_scene import GameScene
            self._scene_manager.set_scene(GameScene(self._scene_manager, level))
        return _play

    def _on_quit(self):
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in (*self._play_buttons.values(), self._quit_button):
                if btn.is_clicked(event.pos):
                    btn.click()

    def update(self):
        for btn in (*self._play_buttons.values(), self._quit_button):
            btn.update()

    # ---------- Render ----------
    def draw(self, screen):
        screen.blit(ui.background(screen.get_size()), (0, 0))
        self._draw_blobs(screen)
        self._draw_header(screen)
        for lvl in LEVELS:
            self._draw_card(screen, lvl)
        self._quit_button.draw(screen)
        ui.text(screen, "© MBG Memory Match — karakter fiktif, semangat anti-koruptor.",
                theme.font("body", 14), theme.INK_MUTED,
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 84))

    def _draw_blobs(self, screen):
        t = (pygame.time.get_ticks() - self._t0) * 0.0006
        blobs = [
            (160, 150, 150, theme.BRAND_PURPLE, 26),
            (880, 120, 130, theme.CARD_PEACH, 30),
            (820, 560, 170, theme.BRAND_BLUE, 22),
            (130, 580, 130, theme.SUCCESS_GREEN, 22),
        ]
        for x, y, r, color, alpha in blobs:
            dy = math.sin(t + x) * 6
            blob = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(blob, (*color, alpha), (r, r), r)
            screen.blit(blob, (x - r, y - r + dy))

    def _draw_header(self, screen):
        float_y = math.sin((pygame.time.get_ticks() - self._t0) * 0.002) * 4
        cx = WINDOW_WIDTH // 2
        ui.text(screen, "PROGRAM MAKAN BERGIZI GRATIS",
                theme.font("body", 15, bold=True), theme.INK_MUTED,
                center=(cx, int(96 + float_y)))
        ui.gradient_text(screen, "MBG Memory Match",
                         theme.font("display", 66, bold=True),
                         theme.BRAND_BLUE, theme.BRAND_PURPLE,
                         center=(cx, int(150 + float_y)))
        ui.text(screen, "Siap mencocokkan paket bergizi? Pilih tantanganmu.",
                theme.font("body", 20), theme.INK,
                center=(cx, int(206 + float_y)))

    def _draw_card(self, screen, lvl):
        rect = self._card_rects[lvl]
        cfg = DIFFICULTY[lvl]
        accent = LEVEL_ACCENT[lvl]
        hover = rect.collidepoint(pygame.mouse.get_pos())

        ui.blit_shadow(screen, rect.center, rect.size, theme.RADIUS_PANEL,
                       alpha=58 if hover else 44, y_offset=12)
        ui.round_rect(screen, rect, theme.SURFACE_WHITE, theme.RADIUS_PANEL)
        ui.round_rect(screen, rect, theme.HAIRLINE, theme.RADIUS_PANEL, width=2)

        cx = rect.centerx

        if lvl == "MEDIUM":
            badge = pygame.Rect(0, 0, 132, 30)
            badge.center = (cx, rect.y - 2)
            ui.blit_shadow(screen, badge.center, badge.size, 15, alpha=40, y_offset=4)
            pill = ui.round_image(ui.horizontal_gradient(badge.size, theme.CARD_PEACH,
                                                         theme.DANGER_RED), 15)
            screen.blit(pill, badge.topleft)
            ui.star(screen, (badge.x + 18, badge.centery), 7, theme.SURFACE_WHITE)
            ui.text(screen, "POPULER", theme.font("display", 16, bold=True),
                    theme.SURFACE_WHITE, center=(badge.centerx + 8, badge.centery))

        # ikon: lingkaran lembut berisi bintang tingkat kesulitan (1–3)
        icon_c = (cx, rect.y + 70)
        disc = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.circle(disc, (*accent, 38), (48, 48), 48)
        screen.blit(disc, (icon_c[0] - 48, icon_c[1] - 48))
        n = LEVEL_STARS[lvl]
        for i in range(n):
            sx = icon_c[0] + (i - (n - 1) / 2) * 26
            ui.star(screen, (sx, icon_c[1]), 11, accent)

        ui.text(screen, LEVEL_LABEL[lvl], theme.font("display", 32, bold=True),
                theme.INK, center=(cx, rect.y + 142))
        ui.text(screen, f"{cfg['cols']} × {cfg['rows']} kartu", theme.font("body", 19),
                theme.INK_MUTED, center=(cx, rect.y + 176))
        ui.text(screen, f"{cfg['pairs']} pasang · {cfg['time']} detik",
                theme.font("body", 16), theme.INK_MUTED, center=(cx, rect.y + 202))

        self._play_buttons[lvl].draw(screen)
