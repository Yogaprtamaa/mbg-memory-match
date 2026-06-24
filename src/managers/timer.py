import pygame


class Timer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def reset(self):
        self.start_time = pygame.time.get_ticks()

    def get_time(self):
        return (pygame.time.get_ticks() - self.start_time) // 1000

    def get_formatted_time(self):
        total_seconds = self.get_time()

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        return f"{minutes:02}:{seconds:02}"