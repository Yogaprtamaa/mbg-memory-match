import random

import pygame

from src.scenes.scene import Scene
from src.objects.button import Button
from src.utils import ui
from src.config import theme
from src.config.constants import WINDOW_WIDTH, WINDOW_HEIGHT

WIN_RESULT = "MENANG"
KORUPTOR_RESULT = "Kena Koruptor!"

CONFETTI_COLORS = [theme.SCORE_GOLD, theme.SUCCESS_GREEN, theme.CARD_PEACH,
                   theme.BRAND_BLUE, theme.BRAND_PURPLE]

# Aksen status mengikuti hasil (design.md §2c)
RESULT_ACCENT = {
    WIN_RESULT: theme.SUCCESS_GREEN,
    KORUPTOR_RESULT: theme.DANGER_RED,
    "Waktu Habis": theme.BRAND_PURPLE,
}


class GameOverScene(Scene):
    """Layar akhir: panel kaca center, status berwarna, statistik, navigasi."""

    def __init__(self, scene_manager, result, score, moves, time_used, level):
        self._scene_manager = scene_manager
        self._result = result
        self._score = score
        self._moves = moves
        self._time_used = time_used
        self._level = level
        self._is_win = result == WIN_RESULT
        self._accent = RESULT_ACCENT.get(result, theme.BRAND_PURPLE)

        self._panel = pygame.Rect(0, 0, 520, 470)
        self._panel.center = (WINDOW_WIDTH // 2, 360)

        bw, bh = 190, 52
        by = self._panel.bottom - 84
        self._buttons = [
            Button(WINDOW_WIDTH // 2 - bw - 10, by, bw, bh, "Main Lagi",
                   self._on_restart, gradient=(theme.SUCCESS_GREEN, (96, 176, 130)),
                   font_size=22),
            Button(WINDOW_WIDTH // 2 + 10, by, bw, bh, "Menu",
                   self._on_menu, color=theme.SURFACE_WHITE,
                   text_color=theme.INK, font_size=22, border_color=theme.HAIRLINE),
        ]

        self._confetti = [self._spawn_confetti(initial=True)
                          for _ in range(140)] if self._is_win else []

    # ---------- Aksi ----------
    def _on_restart(self):
        pygame.mixer.stop()
        from src.scenes.game_scene import GameScene
        self._scene_manager.set_scene(GameScene(self._scene_manager, self._level))

    def _on_menu(self):
        pygame.mixer.stop()
        from src.scenes.menu_scene import MenuScene
        self._scene_manager.set_scene(MenuScene(self._scene_manager))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self._buttons:
                if button.is_clicked(event.pos):
                    button.click()

    # ---------- Confetti ----------
    def _spawn_confetti(self, initial=False):
        return {
            "x": random.uniform(0, WINDOW_WIDTH),
            "y": random.uniform(-WINDOW_HEIGHT, 0) if initial else random.uniform(-40, -10),
            "vy": random.uniform(60, 160) / 60.0,
            "vx": random.uniform(-20, 20) / 60.0,
            "size": random.randint(6, 11),
            "color": random.choice(CONFETTI_COLORS),
            "rot": random.uniform(0, 360),
            "spin": random.uniform(-6, 6),
        }

    def update(self):
        for button in self._buttons:
            button.update()
        for p in self._confetti:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.02
            p["rot"] += p["spin"]
            if p["y"] > WINDOW_HEIGHT + 20:
                p.update(self._spawn_confetti())

    # ---------- Render ----------
    def draw(self, screen):
        screen.blit(ui.background(screen.get_size()), (0, 0))
        if self._result == KORUPTOR_RESULT:
            self._draw_vignette(screen)
        self._draw_confetti(screen)
        self._draw_panel(screen)
        for button in self._buttons:
            button.draw(screen)

    def _draw_vignette(self, screen):
        veil = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        max_r = (WINDOW_WIDTH ** 2 + WINDOW_HEIGHT ** 2) ** 0.5 / 2
        for i in range(8, 0, -1):
            t = i / 8
            r = int(max_r * t)
            a = int(90 * t)
            pygame.draw.circle(veil, (*theme.DANGER_RED, a), (cx, cy), r)
        # lubang terang di tengah
        pygame.draw.circle(veil, (0, 0, 0, 0), (cx, cy), int(max_r * 0.25))
        screen.blit(veil, (0, 0))

    def _draw_confetti(self, screen):
        for p in self._confetti:
            s = p["size"]
            chip = pygame.Surface((s, s), pygame.SRCALPHA)
            chip.fill(p["color"])
            chip = pygame.transform.rotate(chip, p["rot"])
            screen.blit(chip, (p["x"], p["y"]))

    def _draw_panel(self, screen):
        panel = self._panel
        ui.glass_panel(screen, panel, alpha=205)

        cx = panel.centerx
        seal = (cx, panel.y + 66)
        seal_color = theme.SCORE_GOLD if self._is_win else self._accent
        pygame.draw.circle(screen, ui.lerp_color(seal_color, (255, 255, 255), 0.5),
                           (seal[0], seal[1] + 2), 32)
        pygame.draw.circle(screen, seal_color, seal, 30)
        pygame.draw.circle(screen, ui.lerp_color(seal_color, (0, 0, 0), 0.15), seal, 30, 3)
        ui.text(screen, "MBG", theme.font("display", 24, bold=True),
                theme.SURFACE_WHITE, center=seal)

        ui.text(screen, self._result, theme.font("display", 48, bold=True),
                self._accent, center=(cx, panel.y + 134))
        subtitle = ("Gizi tersalurkan. Kerja bagus!" if self._is_win
                    else "Belum berhasil — coba lagi.")
        ui.text(screen, subtitle, theme.font("body", 18), theme.INK_MUTED,
                center=(cx, panel.y + 168))

        rows = [
            ("Skor Akhir", str(self._score)),
            ("Waktu Terpakai", self._time_used),
            ("Langkah", str(self._moves)),
            ("Level", self._level.title()),
        ]
        row_y = panel.y + 206
        for i, (label, value) in enumerate(rows):
            y = row_y + i * 40
            ui.text(screen, label, theme.font("body", 19), theme.INK_MUTED,
                    midleft=(panel.x + 44, y))
            ui.text(screen, value, theme.font("data", 22, bold=True), theme.INK,
                    midright=(panel.right - 44, y))
            if i < len(rows) - 1:
                pygame.draw.line(screen, theme.HAIRLINE,
                                 (panel.x + 44, y + 20), (panel.right - 44, y + 20), 1)
