import random

import pygame

from src.scenes.scene import Scene
from src.objects.button import Button
from src.utils import ui
from src.config import theme
from src.config.constants import WINDOW_WIDTH, WINDOW_HEIGHT

WIN_RESULT = "MENANG"
CONFETTI_COLORS = [theme.GOLD, theme.LEAF, theme.CARROT, theme.SKY, theme.TOMATO]


class GameOverScene(Scene):
    """Layar akhir bergaya kartu nampan: status, statistik, navigasi."""

    def __init__(self, scene_manager, result, score, moves, time_used, level):
        self._scene_manager = scene_manager
        self._result = result
        self._score = score
        self._moves = moves
        self._time_used = time_used
        self._level = level
        self._is_win = result == WIN_RESULT
        self._accent = theme.LEAF if self._is_win else theme.TOMATO

        self._panel = pygame.Rect(0, 0, 560, 470)
        self._panel.center = (WINDOW_WIDTH // 2, 360)

        bw = 200
        by = self._panel.bottom - 78
        self._buttons = [
            Button(WINDOW_WIDTH // 2 - bw - 12, by, bw, 54, "Main Lagi",
                   self._on_restart, theme.LEAF, font_size=24),
            Button(WINDOW_WIDTH // 2 + 12, by, bw, 54, "Menu",
                   self._on_menu, theme.TRAY, hover_color=(244, 238, 224),
                   text_color=theme.SPINACH, font_size=24, border_color=theme.TRAY_LINE),
        ]

        self._confetti = [self._spawn_confetti(initial=True) for _ in range(140)] if self._is_win else []

    # ---------- Aksi ----------
    def _on_restart(self):
        pygame.mixer.stop()  # hentikan win.mp3/error.mp3 sebelum pindah
        from src.scenes.game_scene import GameScene
        self._scene_manager.set_scene(GameScene(self._scene_manager, self._level))

    def _on_menu(self):
        pygame.mixer.stop()  # hentikan win.mp3/error.mp3 sebelum pindah
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
        screen.blit(ui.vertical_gradient(screen.get_size(), theme.RICE_TOP, theme.RICE_BOT), (0, 0))
        self._draw_confetti(screen)
        self._draw_panel(screen)
        for button in self._buttons:
            button.draw(screen)

    def _draw_confetti(self, screen):
        for p in self._confetti:
            s = p["size"]
            chip = pygame.Surface((s, s), pygame.SRCALPHA)
            chip.fill(p["color"])
            chip = pygame.transform.rotate(chip, p["rot"])
            screen.blit(chip, (p["x"], p["y"]))

    def _draw_panel(self, screen):
        panel = self._panel
        ui.blit_shadow(screen, panel.center, panel.size, 22, alpha=110, y_offset=14)
        ui.round_rect(screen, panel, theme.TRAY, 22)
        ui.round_rect(screen, (panel.x, panel.y, panel.width, 12), self._accent, 22)
        ui.round_rect(screen, panel, theme.TRAY_LINE, 22, width=2)

        cx = panel.centerx
        seal = (cx, panel.y + 70)
        seal_color = theme.GOLD if self._is_win else (120, 120, 120)
        pygame.draw.circle(screen, seal_color, seal, 30)
        pygame.draw.circle(screen, ui.lerp_color(seal_color, (0, 0, 0), 0.2), seal, 30, 3)
        ui.text(screen, "MBG", theme.font("display", 26, bold=True), theme.SPINACH, center=seal)

        ui.text(screen, self._result, theme.font("display", 54, bold=True),
                self._accent, center=(cx, panel.y + 132))
        subtitle = "Gizi tersalurkan. Kerja bagus!" if self._is_win else "Belum berhasil — coba lagi."
        ui.text(screen, subtitle, theme.font("body", 19), theme.SPINACH_SOFT,
                center=(cx, panel.y + 168))

        rows = [
            ("Skor Akhir", str(self._score)),
            ("Waktu Terpakai", self._time_used),
            ("Langkah", str(self._moves)),
            ("Level", self._level.title()),
        ]
        row_y = panel.y + 204
        for i, (label, value) in enumerate(rows):
            y = row_y + i * 42
            ui.text(screen, label, theme.font("body", 20), theme.SPINACH_SOFT,
                    midleft=(panel.x + 48, y))
            ui.text(screen, value, theme.font("mono", 22, bold=True), theme.SPINACH,
                    midright=(panel.right - 48, y))
            if i < len(rows) - 1:
                pygame.draw.line(screen, theme.TRAY_LINE,
                                 (panel.x + 48, y + 21), (panel.right - 48, y + 21), 1)
