import random
import pygame
from config.constants import CARD_VALUES, TRAP_KORUPTOR, TRAP_TERCEMAR, WINDOW_WIDTH, WINDOW_HEIGHT
from config.settings import DIFFICULTY_SETTINGS

class Board:
    def __init__(self, difficulty_level):
        self.level = difficulty_level
        self.config = DIFFICULTY_SETTINGS[difficulty_level]
        self.rows = self.config["rows"]
        self.cols = self.config["cols"]
        self.cards = []
        self.selected_cards = []  
        
       
        self.card_width = 90
        self.card_height = 120
        self.margin = 15
        
       
        try:
            self.sound_match = pygame.mixer.Sound("assets/sounds/match.mp3")
            self.sound_wrong = pygame.mixer.Sound("assets/sounds/error.mp3")
            self.sound_trap = pygame.mixer.Sound("assets/sounds/trap.mp3")
        except pygame.error:
            self.sound_match = None
            self.sound_wrong = None
            self.sound_trap = None
        
        self.generate_board()

    def generate_board(self):
        
        num_pairs = self.config["pairs"]
        chosen_values = random.sample(CARD_VALUES, num_pairs)
        
        pool = chosen_values * 2
        pool.append(TRAP_KORUPTOR)
        pool.append(TRAP_TERCEMAR)
        random.shuffle(pool)
        
        total_grid_width = (self.cols * self.card_width) + ((self.cols - 1) * self.margin)
        total_grid_height = (self.rows * self.card_height) + ((self.rows - 1) * self.margin)
        
        start_x = (WINDOW_WIDTH - total_grid_width) // 2
        start_y = ((WINDOW_HEIGHT - 100) - total_grid_height) // 2 + 80
        
        idx = 0
        for r in range(self.rows):
            for c in range(self.cols):
                x = start_x + c * (self.card_width + self.margin)
                y = start_y + r * (self.card_height + self.margin)
                
                card_val = pool[idx]
                
                
                from src.cards.card import Card
                card = Card(card_val, x, y, self.card_width, self.card_height)
                
                self.cards.append(card)
                idx += 1

    def get_card_at(self, pos):
        
        for card in self.cards:
            if card.rect.collidepoint(pos):
                return card
        return None

    def select_card(self, card):
        
        if card in self.selected_cards or card.is_flipped or len(self.selected_cards) >= 2:
            return
            
        card.flip()  
        self.selected_cards.append(card)
        
        if len(self.selected_cards) == 2:
            self.check_match()

    def check_match(self):
       
        card1, card2 = self.selected_cards[0], self.selected_cards[1]
        
       
        if getattr(card1, 'is_trap', False) or getattr(card2, 'is_trap', False) or card1.value in [TRAP_KORUPTOR, TRAP_TERCEMAR] or card2.value in [TRAP_KORUPTOR, TRAP_TERCEMAR]:
            if self.sound_trap:
                self.sound_trap.play()
            print("GAME OVER: Terkena Perangkap!")
            return

       
        if card1.value == card2.value:
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

    def draw(self, screen):
        for card in self.cards:
            card.draw(screen)