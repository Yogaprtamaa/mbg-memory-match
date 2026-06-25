import pygame
<<<<<<< HEAD
from config.constants import LEVEL_EASY, LEVEL_MEDIUM, LEVEL_HARD, COLOR_TEXT, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_WHITE

class MenuScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.selected_level = LEVEL_EASY # Default level awal
        
        # Koordinat sederhana tombol Level Box
        self.btn_easy = pygame.Rect(250, 400, 140, 50)
        self.btn_medium = pygame.Rect(430, 400, 140, 50)
        self.btn_hard = pygame.Rect(610, 400, 140, 50)
        
        # Tombol Play Utama
        self.btn_play = pygame.Rect(400, 520, 200, 60)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Cek pemilihan level kesulitan
            if self.btn_easy.collidepoint(mouse_pos):
                self.selected_level = LEVEL_EASY
            elif self.btn_medium.collidepoint(mouse_pos):
                self.selected_level = LEVEL_MEDIUM
            elif self.btn_hard.collidepoint(mouse_pos):
                self.selected_level = LEVEL_HARD
                
            # Cek jika tombol Play diklik
            elif self.btn_play.collidepoint(mouse_pos):
                # Fitur 1 & 4 Linker: Kirim level pilihan ke GameScene baru
                # self.scene_manager.set_scene(GameScene(self.selected_level))
                print(f"Memulai permainan dengan tingkat kesulitan: {self.selected_level}")

    def update(self):
        pass

    def draw(self, screen):
        # Render Judul Menu
        font_title = pygame.font.SysFont(None, 64)
        title_text = font_title.render("MBG Memory Match", True, COLOR_TEXT)
        screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 150))
        
        font_sub = pygame.font.SysFont(None, 32)
        sub_text = font_sub.render("Pilih Tingkat Kesulitan:", True, COLOR_TEXT)
        screen.blit(sub_text, (WINDOW_WIDTH//2 - sub_text.get_width()//2, 340))

        # Render Tombol Kesulitan (Highlight jika terpilih)
        self._draw_level_button(screen, self.btn_easy, "Easy", self.selected_level == LEVEL_EASY)
        self._draw_level_button(screen, self.btn_medium, "Medium", self.selected_level == LEVEL_MEDIUM)
        self._draw_level_button(screen, self.btn_hard, "Hard", self.selected_level == LEVEL_HARD)

        # Render Tombol Play
        pygame.draw.rect(screen, COLOR_PRIMARY, self.btn_play, border_radius=10)
        font_play = pygame.font.SysFont(None, 40)
        play_text = font_play.render("MULAI", True, COLOR_WHITE)
        screen.blit(play_text, (self.btn_play.centerx - play_text.get_width()//2, self.btn_play.centery - play_text.get_height()//2))

    def _draw_level_button(self, screen, rect, text, is_selected):
        color = COLOR_PRIMARY if is_selected else COLOR_SECONDARY
        width = 0 if is_selected else 2 # Blok penuh jika terpilih, border jika tidak
        
        if is_selected:
            pygame.draw.rect(screen, color, rect, border_radius=5)
            text_color = COLOR_WHITE
        else:
            pygame.draw.rect(screen, color, rect, width=width, border_radius=5)
            text_color = color
            
        font = pygame.font.SysFont(None, 28)
        lbl = font.render(text, True, text_color)
        screen.blit(lbl, (rect.centerx - lbl.get_width()//2, rect.centery - lbl.get_height()//2))
=======
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
>>>>>>> c98a386 (feat: implement game architecture, scene management, and base card logic with trap support and finish fitur 1 and 2)
