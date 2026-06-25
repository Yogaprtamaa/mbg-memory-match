<<<<<<< HEAD
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
=======
import pygame
from src.cards.card import Card

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cards = []  
        self.selected_cards = [] 
        
       
        try:
            self.sound_match = pygame.mixer.Sound("assets/sounds/match.wav")
            self.sound_wrong = pygame.mixer.Sound("assets/sounds/wrong.wav")
            self.sound_trap = pygame.mixer.Sound("assets/sounds/trap.wav")
        except pygame.error:
            self.sound_match = None
            self.sound_wrong = None
            self.sound_trap = None

    def select_card(self, card):
        
        if card in self.selected_cards or card.is_flipped or len(self.selected_cards) >= 2:
            return
            
        card.flip()  
        self.selected_cards.append(card)
        
        
        if len(self.selected_cards) == 2:
            self.check_match()

    def check_match(self):
        
        card1, card2 = self.selected_cards[0], self.selected_cards[1]
        
        
        if getattr(card1, 'is_trap', False) or getattr(card2, 'is_trap', False):
            if self.sound_trap:
                self.sound_trap.play()
            print("GAME OVER: Terkena Oknum Koruptor!")
          
            return

        
        if card1.front_image == card2.front_image: 
            if self.sound_match:
                self.sound_match.play()
            card1.is_matched = True
            card2.is_matched = True
            self.selected_cards.clear()  
            
       
        else:
            if self.sound_wrong:
                self.sound_wrong.play()
            
            card1.flip()
            card2.flip()
            self.selected_cards.clear()

    def update(self):
        
        for card in self.cards:
            card.update()

    def draw(self, surface):
        
        for card in self.cards:
            card.draw(surface)
>>>>>>> 374bf845542417eba8237d9dd3aa3a2f424a703b
