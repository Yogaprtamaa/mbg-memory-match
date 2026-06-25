import random
import pygame
from config.constants import CARD_VALUES, TRAP_KORUPTOR, TRAP_TERCEMAR, WINDOW_WIDTH, WINDOW_HEIGHT
from config.settings import DIFFICULTY_SETTINGS

# Dummy imports/placeholders untuk Card subclasses agar tidak Error saat inisialisasi
# Nantinya akan di-import nyata dari src.cards
class DummyCard:
    def __init__(self, value, x=0, y=0, w=80, h=110):
        self.value = value
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self, screen):
        pygame.draw.rect(screen, (52, 152, 219), self.rect, border_radius=8)

class Board:
    def __init__(self, difficulty_level):
        self.level = difficulty_level
        self.config = DIFFICULTY_SETTINGS[difficulty_level]
        self.rows = self.config["rows"]
        self.cols = self.config["cols"]
        self.cards = []
        
        # Dimensi kartu default
        self.card_width = 90
        self.card_height = 120
        self.margin = 15
        
        self.generate_board()

    def generate_board(self):
        # 1. Kumpulkan pool kartu sesuai kapasitas spek PRD
        num_pairs = self.config["pairs"]
        chosen_values = random.sample(CARD_VALUES, num_pairs)
        
        # Duplikat untuk membuat pasangan match
        pool = chosen_values * 2
        
        # Tambahkan trap wajib (1 Koruptor + 1 Tercemar)
        pool.append(TRAP_KORUPTOR)
        pool.append(TRAP_TERCEMAR)
        
        # Acak seluruh isi pool kartu
        random.shuffle(pool)
        
        # 2. Kalkulasi Auto-Layout Grid Center Matrix
        # Hitung total dimensi grid untuk centering otomatis
        total_grid_width = (self.cols * self.card_width) + ((self.cols - 1) * self.margin)
        total_grid_height = (self.rows * self.card_height) + ((self.rows - 1) * self.margin)
        
        # Koordinat start (Top-Left) agar posisi grid pas di tengah screen
        start_x = (WINDOW_WIDTH - total_grid_width) // 2
        start_y = ((WINDOW_HEIGHT - 100) - total_grid_height) // 2 + 80 # Sisa ruang untuk bar HUD timer/skor di atas
        
        # 3. Distribusikan kartu ke koordinat grid
        idx = 0
        for r in range(self.rows):
            for c in range(self.cols):
                x = start_x + c * (self.card_width + self.margin)
                y = start_y + r * (self.card_height + self.margin)
                
                card_val = pool[idx]
                
                # TODO: Ganti DummyCard dengan class instansiasi riil dari Phase 2
                # Contoh: if card_val == TRAP_KORUPTOR: card = KoruptorCard(x, y) dst.
                card = DummyCard(card_val, x, y, self.card_width, self.card_height)
                
                self.cards.append(card)
                idx += 1

    def get_card_at(self, pos):
        """Mendeteksi klik mouse pada kartu tertentu"""
        for card in self.cards:
            if card.rect.collidepoint(pos):
                return card
        return None

    def draw(self, screen):
        for card in self.cards:
            card.draw(screen)