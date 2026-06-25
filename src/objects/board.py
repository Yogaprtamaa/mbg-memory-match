import random
<<<<<<< HEAD
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
=======
import os
from src.cards.match_card import MatchCard
from src.cards.koruptor_card import KoruptorCard
from src.cards.tercemar_card import TercemarCard
from src.config.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, HUD_HEIGHT,
    CARD_WIDTH, CARD_HEIGHT, CARD_MARGIN,
    MATCH_VALUES, CARD_FRONT_COLORS,
)
from src.config.settings import DIFFICULTY, IMAGE_PATH


class Board:

    def __init__(self, level):
        config = DIFFICULTY[level]
        self._rows = config["rows"]
        self._cols = config["cols"]
        self._cards = []
        self._generate(config)

    def _generate(self, config):
        values = MATCH_VALUES[:config["pairs"]]
        card_data = []

        for i, value in enumerate(values):
            color = CARD_FRONT_COLORS[i % len(CARD_FRONT_COLORS)]
            card_data.append((value, color, "match"))
            card_data.append((value, color, "match"))

        card_data.append((None, None, "koruptor"))
        card_data.append((None, None, "tercemar"))

        random.shuffle(card_data)

        positions = self._calculate_positions()

        back_path = os.path.join(IMAGE_PATH, "card_back.png")

        for idx, (x, y) in enumerate(positions):
            value, color, card_type = card_data[idx]

            if card_type == "koruptor":
                front_path = os.path.join(IMAGE_PATH, "traps", "koruptor.png")
                card = KoruptorCard(x, y, CARD_WIDTH, CARD_HEIGHT,
                                    front_path, back_path)
            elif card_type == "tercemar":
                front_path = os.path.join(IMAGE_PATH, "traps", "makanan_tercemar.png")
                card = TercemarCard(x, y, CARD_WIDTH, CARD_HEIGHT,
                                    front_path, back_path)
            else:
                front_path = os.path.join(IMAGE_PATH, "cards", f"{value}.png")
                card = MatchCard(x, y, CARD_WIDTH, CARD_HEIGHT, value,
                                 front_path, back_path, color)

            self._cards.append(card)

    def _calculate_positions(self):
        grid_w = self._cols * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN
        grid_h = self._rows * (CARD_HEIGHT + CARD_MARGIN) - CARD_MARGIN

        start_x = (WINDOW_WIDTH - grid_w) // 2
        start_y = HUD_HEIGHT + (WINDOW_HEIGHT - HUD_HEIGHT - grid_h) // 2

        positions = []
        for row in range(self._rows):
            for col in range(self._cols):
                x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
                y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
                positions.append((x, y))
        return positions

    def get_card_at(self, pos):
        for card in self._cards:
>>>>>>> c98a386 (feat: implement game architecture, scene management, and base card logic with trap support and finish fitur 1 and 2)
            if card.rect.collidepoint(pos):
                return card
        return None

<<<<<<< HEAD
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
=======
    def all_matched(self):
        for card in self._cards:
            if isinstance(card, MatchCard) and not card.is_matched:
                return False
        return True

    def update(self):
        for card in self._cards:
            card.update()

    def draw(self, screen):
        for card in self._cards:
            card.draw(screen)
>>>>>>> c98a386 (feat: implement game architecture, scene management, and base card logic with trap support and finish fitur 1 and 2)
