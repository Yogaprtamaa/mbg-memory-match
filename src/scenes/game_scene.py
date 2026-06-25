import pygame
from src.scenes.scene import Scene
from src.objects.board import Board
from src.managers.score_manager import ScoreManager
from src.managers.timer import Timer
from src.cards.flip_result import FlipResult
from src.utils.asset_loader import get_asset_loader
from src.utils import ui
from src.config import theme
from src.config.constants import (
    WINDOW_WIDTH, HUD_HEIGHT,
    SCORE_MATCH, SCORE_MISMATCH, SCORE_TRAP_PENALTY,
    TIMER_TRAP_PENALTY, BONUS_MULTIPLIER, MISMATCH_DELAY,
)
from src.config.settings import DIFFICULTY, SOUND_PATH

LEVEL_TINT = {"EASY": theme.LEAF, "MEDIUM": theme.CARROT, "HARD": theme.TOMATO}

SOUND_MATCH = SOUND_PATH + "match.mp3"
SOUND_TRAP = SOUND_PATH + "trap.mp3"
SOUND_WIN = SOUND_PATH + "win.mp3"
SOUND_GAME_OVER = SOUND_PATH + "error.mp3"

WIN_REASON = "MENANG"

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

    def handle_event(self, event):
        if self._game_over:
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
        if self._game_over:
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

    def draw(self, screen):
        screen.blit(ui.vertical_gradient(screen.get_size(), theme.RICE_TOP, theme.RICE_BOT), (0, 0))
        self._board.draw(screen)
        self._draw_hud(screen)

    def _draw_hud(self, screen):
        strip = pygame.Rect(0, 0, WINDOW_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(screen, theme.TRAY, strip)
        pygame.draw.line(screen, theme.TRAY_LINE, (0, HUD_HEIGHT), (WINDOW_WIDTH, HUD_HEIGHT), 2)

        # Skor (kiri)
        ui.text(screen, "SKOR", theme.font("body", 14, bold=True), theme.SPINACH_SOFT,
                topleft=(30, 16))
        ui.text(screen, str(self._score_manager.score), theme.font("mono", 34, bold=True),
                theme.SPINACH, topleft=(30, 36))

        # Langkah (kanan)
        ui.text(screen, "LANGKAH", theme.font("body", 14, bold=True), theme.SPINACH_SOFT,
                midright=(WINDOW_WIDTH - 30, 24))
        ui.text(screen, str(self._score_manager.moves), theme.font("mono", 34, bold=True),
                theme.SPINACH, midright=(WINDOW_WIDTH - 30, 54))

        # Timer + bar kesegaran (tengah)
        self._draw_timer(screen)

    def _draw_timer(self, screen):
        cx = WINDOW_WIDTH // 2
        ratio = self._timer.remaining / max(1, self._timer.total)

        if ratio > 0.5:
            color = ui.lerp_color(theme.CARROT, theme.LEAF, (ratio - 0.5) * 2)
        else:
            color = ui.lerp_color(theme.TOMATO, theme.CARROT, ratio * 2)

        pill = LEVEL_TINT.get(self._level, theme.LEAF)
        ui.text(screen, self._level, theme.font("body", 13, bold=True), pill,
                center=(cx, 16))
        ui.text(screen, self._timer.get_formatted_time(),
                theme.font("mono", 38, bold=True), color, center=(cx, 42))

        bar_w, bar_h, bar_y = 280, 8, 66
        track = pygame.Rect(cx - bar_w // 2, bar_y, bar_w, bar_h)
        ui.round_rect(screen, track, theme.TRAY_LINE, bar_h // 2)
        fill_w = int(bar_w * max(0.0, min(1.0, ratio)))
        if fill_w > 0:
            ui.round_rect(screen, pygame.Rect(track.x, bar_y, fill_w, bar_h), color, bar_h // 2)
