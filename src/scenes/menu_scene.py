import pygame
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