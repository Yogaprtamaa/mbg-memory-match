import pygame


class Timer:
    def __init__(self, total_seconds):
        self._total = total_seconds
        self._remaining = float(total_seconds)
        self._last_tick = None

    @property
    def remaining(self):
        return self._remaining

    def start(self):
        self._last_tick = pygame.time.get_ticks()

    def tick(self):
        now = pygame.time.get_ticks()
        if self._last_tick is not None:
            dt = (now - self._last_tick) / 1000.0
            self._remaining = max(0.0, self._remaining - dt)
        self._last_tick = now

    def subtract(self, seconds):
        self._remaining = max(0.0, self._remaining - seconds)

    def is_expired(self):
        return self._remaining <= 0

    def get_formatted_time(self):
        total = int(self._remaining)
        minutes = total // 60
        seconds = total % 60
        return f"{minutes:02}:{seconds:02}"

    def reset(self, total_seconds=None):
        if total_seconds is not None:
            self._total = total_seconds
        self._remaining = float(self._total)
        self._last_tick = None
