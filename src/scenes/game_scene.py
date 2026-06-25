import pygame
from src.scenes.scene import Scene
from src.objects.board import Board
from src.managers.score_manager import ScoreManager
from src.managers.timer import Timer
from src.cards.trap_card import TrapCard
from src.config.constants import (
    WINDOW_WIDTH, BG_COLOR, BLACK, WHITE, RED,
    SCORE_MATCH, SCORE_MISMATCH, SCORE_TRAP_PENALTY,
    TIMER_TRAP_PENALTY, BONUS_MULTIPLIER, MISMATCH_DELAY,
)
from src.config.settings import DIFFICULTY

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

        self._state = IDLE
        self._first_pick = None
        self._second_pick = None
        self._flip_back_time = 0
        self._game_over = False

        self._hud_font = pygame.font.SysFont(None, 36)

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

        if self._state == FIRST_ANIMATING:
            if not self._first_pick.is_animating:
                result = self._first_pick.on_flip()
                if result == "GAME_OVER":
                    self._end_game("Kena Koruptor!")
                elif result == "PENALTY":
                    self._score_manager.penalty(abs(SCORE_TRAP_PENALTY))
                    self._timer.subtract(TIMER_TRAP_PENALTY)
                    self._flip_back_time = pygame.time.get_ticks() + MISMATCH_DELAY
                    self._state = SHOWING_RESULT
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
        if result == "GAME_OVER":
            self._end_game("Kena Koruptor!")
            return
        if result == "PENALTY":
            self._score_manager.penalty(abs(SCORE_TRAP_PENALTY))
            self._timer.subtract(TIMER_TRAP_PENALTY)
            self._flip_back_time = pygame.time.get_ticks() + MISMATCH_DELAY
            self._state = SHOWING_RESULT
            return

        if c1.value == c2.value:
            c1.is_matched = True
            c2.is_matched = True
            self._score_manager.add_score(SCORE_MATCH)
            self._reset_picks()

            if self._board.all_matched():
                bonus = int(self._timer.remaining) * BONUS_MULTIPLIER
                self._score_manager.add_score(bonus)
                self._end_game("MENANG")
        else:
            self._score_manager.add_score(SCORE_MISMATCH)
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
        from src.scenes.menu_scene import MenuScene
        self._scene_manager.set_scene(MenuScene(self._scene_manager))

    def draw(self, screen):
        screen.fill(BG_COLOR)
        self._draw_hud(screen)
        self._board.draw(screen)

    def _draw_hud(self, screen):
        score_text = self._hud_font.render(
            f"Skor: {self._score_manager.score}", True, BLACK
        )
        screen.blit(score_text, (20, 15))

        timer_color = RED if self._timer.remaining <= 10 else BLACK
        timer_text = self._hud_font.render(
            self._timer.get_formatted_time(), True, timer_color
        )
        timer_rect = timer_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        screen.blit(timer_text, timer_rect)

        moves_text = self._hud_font.render(
            f"Moves: {self._score_manager.moves}", True, BLACK
        )
        moves_rect = moves_text.get_rect(topright=(WINDOW_WIDTH - 20, 15))
        screen.blit(moves_text, moves_rect)

        level_text = pygame.font.SysFont(None, 24).render(
            f"Level: {self._level}", True, (100, 100, 100)
        )
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(level_text, level_rect)
