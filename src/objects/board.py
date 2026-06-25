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