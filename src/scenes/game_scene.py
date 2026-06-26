import math

import pygame

from src.scenes.scene import Scene
from src.objects.board import Board
from src.objects.button import Button
from src.managers.score_manager import ScoreManager
from src.managers.timer import Timer
from src.cards.flip_result import FlipResult
from src.utils.asset_loader import get_asset_loader
from src.utils import ui
from src.config import theme
from src.config.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MARGIN, HUD_PANEL_W, BOARD_TOP,
    SCORE_MATCH, SCORE_MISMATCH, SCORE_TRAP_PENALTY,
    TIMER_TRAP_PENALTY, BONUS_MULTIPLIER, MISMATCH_DELAY,
)
from src.config.settings import DIFFICULTY, SOUND_PATH

SOUND_MATCH = SOUND_PATH + "match.mp3"
SOUND_TRAP = SOUND_PATH + "trap.mp3"
SOUND_WIN = SOUND_PATH + "win.mp3"
SOUND_GAME_OVER = SOUND_PATH + "error.mp3"

WIN_REASON = "MENANG"
DANGER_SECONDS = 10

IDLE = 0
FIRST_ANIMATING = 1
WAITING_SECOND = 2
SECOND_ANIMATING = 3
SHOWING_RESULT = 4


class GameScene(Scene):

    def __init__(self, scene_manager, level):
        self._scene_manager = scene_manager
        self._level = level
        config = DIFFICULTY[level]

        self._board = Board(level)
        self._score_manager = ScoreManager()
        self._timer = Timer(config["time"])
        self._timer.start()
        self._loader = get_asset_loader()

        self._state = IDLE
        self._first_pick = None
        self._second_pick = None
        self._flip_back_time = 0
        self._game_over = False
        self._paused = False

        # Pill kanan-atas (design.md §2b)
        pw, ph, gap = 104, 40, 12
        right = WINDOW_WIDTH - WINDOW_MARGIN
        self._pause_btn = Button(
            right - pw, 30, pw, ph, "Jeda", self._toggle_pause,
            color=theme.SURFACE_WHITE, text_color=theme.INK,
            font_size=18, border_color=theme.HAIRLINE)
        self._menu_btn = Button(
            right - pw * 2 - gap, 30, pw, ph, "Menu", self._on_menu,
            color=theme.SURFACE_WHITE, text_color=theme.INK,
            font_size=18, border_color=theme.HAIRLINE)
        self._buttons = [self._menu_btn, self._pause_btn]

        self._panel = pygame.Rect(WINDOW_MARGIN, BOARD_TOP, HUD_PANEL_W,
                                  WINDOW_HEIGHT - BOARD_TOP - WINDOW_MARGIN)

    # ---------- Aksi tombol ----------
    def _toggle_pause(self):
        if self._game_over:
            return
        self._paused = not self._paused
        self._pause_btn.text = "Lanjut" if self._paused else "Jeda"
        if not self._paused:
            self._timer.start()  # resync agar waktu jeda tidak terpotong

    def _on_menu(self):
        pygame.mixer.stop()
        from src.scenes.menu_scene import MenuScene
        self._scene_manager.set_scene(MenuScene(self._scene_manager))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self._buttons:
                if btn.is_clicked(event.pos):
                    btn.click()
                    return

        if self._game_over or self._paused:
            return
        if self._state not in (IDLE, WAITING_SECOND):
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        card = self._board.get_card_at(event.pos)
        if not card or card.is_flipped or card.is_matched or card.is_animating:
            return

        card.flip()
        if self._state == IDLE:
            self._first_pick = card
            self._state = FIRST_ANIMATING
        else:
            self._second_pick = card
            self._state = SECOND_ANIMATING

    def update(self):
        for btn in self._buttons:
            btn.update()
        if self._game_over or self._paused:
            return

        self._timer.tick()
        if self._timer.is_expired():
            self._end_game("Waktu Habis")
            return

        self._board.update()
        interactive = self._state in (IDLE, WAITING_SECOND)
        self._board.update_hover(pygame.mouse.get_pos(), interactive)

        if self._state == FIRST_ANIMATING:
            if not self._first_pick.is_animating:
                result = self._first_pick.on_flip()
                if result == FlipResult.GAME_OVER:
                    self._end_game("Kena Koruptor!")
                elif result == FlipResult.PENALTY:
                    self._apply_trap_penalty()
                else:
                    self._state = WAITING_SECOND

        elif self._state == SECOND_ANIMATING:
            if not self._second_pick.is_animating:
                self._evaluate_pair()

        elif self._state == SHOWING_RESULT:
            if pygame.time.get_ticks() >= self._flip_back_time:
                self._do_flip_back()

    def _evaluate_pair(self):
        c1, c2 = self._first_pick, self._second_pick
        self._score_manager.add_move()

        result = c2.on_flip()
        if result == FlipResult.GAME_OVER:
            self._end_game("Kena Koruptor!")
            return
        if result == FlipResult.PENALTY:
            self._apply_trap_penalty()
            return

        if c1.value == c2.value:
            c1.mark_matched()
            c2.mark_matched()
            self._score_manager.add_score(SCORE_MATCH)
            self._loader.play_sound(SOUND_MATCH)
            self._reset_picks()

            if self._board.all_matched():
                bonus = int(self._timer.remaining) * BONUS_MULTIPLIER
                self._score_manager.add_score(bonus)
                self._end_game(WIN_REASON)
        else:
            self._score_manager.add_score(SCORE_MISMATCH)
            self._start_flip_back_delay()

    def _apply_trap_penalty(self):
        self._score_manager.penalty(abs(SCORE_TRAP_PENALTY))
        self._timer.subtract(TIMER_TRAP_PENALTY)
        self._loader.play_sound(SOUND_TRAP)
        self._start_flip_back_delay()

    def _start_flip_back_delay(self):
        self._flip_back_time = pygame.time.get_ticks() + MISMATCH_DELAY
        self._state = SHOWING_RESULT

    def _do_flip_back(self):
        if self._first_pick and not self._first_pick.is_matched:
            self._first_pick.flip()
        if self._second_pick and not self._second_pick.is_matched:
            self._second_pick.flip()
        self._reset_picks()

    def _reset_picks(self):
        self._first_pick = None
        self._second_pick = None
        self._flip_back_time = 0
        self._state = IDLE

    def _end_game(self, reason):
        self._game_over = True
        self._loader.play_sound(SOUND_WIN if reason == WIN_REASON else SOUND_GAME_OVER)

        from src.scenes.game_over_scene import GameOverScene
        time_used = Timer.format_seconds(self._timer.elapsed)
        self._scene_manager.set_scene(GameOverScene(
            self._scene_manager, reason,
            self._score_manager.score, self._score_manager.moves,
            time_used, self._level,
        ))

    # ---------- Render ----------
    def draw(self, screen):
        screen.blit(ui.background(screen.get_size()), (0, 0))
        self._board.draw(screen)
        self._draw_header(screen)
        self._draw_hud(screen)
        for btn in self._buttons:
            btn.draw(screen)
        if self._paused:
            self._draw_pause_overlay(screen)

    def _draw_header(self, screen):
        ui.gradient_text(screen, "MBG Memory Match", theme.font("display", 24, bold=True),
                         theme.BRAND_BLUE, theme.BRAND_PURPLE,
                         midleft=(WINDOW_MARGIN, 50))

    def _draw_hud(self, screen):
        panel = self._panel
        ui.glass_panel(screen, panel)

        cx = panel.centerx
        # tiga blok statistik
        self._stat(screen, cx, panel.y + 56, "star", theme.SCORE_GOLD, "SKOR",
                   str(self._score_manager.score), theme.INK)

        self._stat(screen, cx, panel.y + 168, "card", theme.BRAND_PURPLE, "PASANGAN",
                   f"{self._board.matched_pairs} / {self._board.total_pairs}", theme.INK)

        self._draw_timer(screen, cx, panel.y + 280)

    def _draw_icon(self, screen, kind, center, color):
        cx, cy = center
        if kind == "star":
            ui.star(screen, center, 13, color)
        elif kind == "card":
            r1 = pygame.Rect(cx - 13, cy - 11, 16, 22)
            r2 = pygame.Rect(cx - 4, cy - 11, 16, 22)
            ui.round_rect(screen, r1, ui.lerp_color(color, (255, 255, 255), 0.45), 4)
            ui.round_rect(screen, r2, color, 4)
            ui.round_rect(screen, r2, theme.SURFACE_WHITE, 4, width=2)
        elif kind == "clock":
            pygame.draw.circle(screen, color, center, 13, 3)
            pygame.draw.line(screen, color, center, (cx, cy - 8), 3)
            pygame.draw.line(screen, color, center, (cx + 6, cy + 2), 3)

    def _stat(self, screen, cx, y, kind, icon_color, label, value, value_color, value_size=40):
        self._draw_icon(screen, kind, (cx, y - 16), icon_color)
        ui.text(screen, label, theme.font("body", 14, bold=True), theme.INK_MUTED,
                center=(cx, y + 8))
        ui.text(screen, value, theme.font("data", value_size, bold=True), value_color,
                center=(cx, y + 44))

    def _draw_timer(self, screen, cx, y):
        remaining = self._timer.remaining
        danger = remaining <= DANGER_SECONDS
        color = theme.DANGER_RED if danger else theme.INK
        size = 40
        if danger:
            size = 40 + int(4 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.006)))

        self._draw_icon(screen, "clock", (cx, y - 16),
                        theme.DANGER_RED if danger else theme.BRAND_BLUE)
        ui.text(screen, "WAKTU", theme.font("body", 14, bold=True), theme.INK_MUTED,
                center=(cx, y + 8))
        ui.text(screen, self._timer.get_formatted_time(),
                theme.font("data", size, bold=True), color, center=(cx, y + 44))

        # bar kesegaran
        ratio = max(0.0, min(1.0, remaining / max(1, self._timer.total)))
        bar_w, bar_h = HUD_PANEL_W - 64, 8
        track = pygame.Rect(cx - bar_w // 2, y + 72, bar_w, bar_h)
        ui.round_rect(screen, track, theme.HAIRLINE, bar_h // 2)
        fill_w = int(bar_w * ratio)
        if fill_w > 0:
            fill_c = theme.DANGER_RED if danger else theme.SUCCESS_GREEN
            ui.round_rect(screen, pygame.Rect(track.x, track.y, fill_w, bar_h),
                          fill_c, bar_h // 2)

    def _draw_pause_overlay(self, screen):
        veil = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        veil.fill((233, 224, 246, 165))
        screen.blit(veil, (0, 0))
        cx = WINDOW_WIDTH // 2
        ui.gradient_text(screen, "Jeda", theme.font("display", 72, bold=True),
                         theme.BRAND_BLUE, theme.BRAND_PURPLE, center=(cx, 320))
        ui.text(screen, "Klik \"Lanjut\" untuk meneruskan permainan.",
                theme.font("body", 20), theme.INK, center=(cx, 378))
