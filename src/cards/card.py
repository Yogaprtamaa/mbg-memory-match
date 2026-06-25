import pygame

class Card:
    def __init__(self, value, x, y, width, height):
        self.value = value
        self.rect = pygame.Rect(x, y, width, height)
        self.is_flipped = False
        self.is_matched = False
        
      
        from config.constants import TRAP_KORUPTOR, TRAP_TERCEMAR
        self.is_trap = value in [TRAP_KORUPTOR, TRAP_TERCEMAR]
        
       
        try:
            self.sound_flip = pygame.mixer.Sound("assets/sounds/flip.mp3")
        except pygame.error:
            self.sound_flip = None

    def flip(self):
       
        self.is_flipped = not self.is_flipped
        if self.sound_flip:
            self.sound_flip.play()

    def update(self):
        
        pass

    def draw(self, screen):
        
        if self.is_matched:
          
            return
            
        if self.is_flipped:
           
            pygame.draw.rect(screen, (230, 230, 230), self.rect, border_radius=8)
           
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
        else:
            
            pygame.draw.rect(screen, (52, 152, 219), self.rect, border_radius=8)
            pygame.draw.rect(screen, (41, 128, 185), self.rect, width=3, border_radius=8)