from abc import ABC, abstractmethod
import pygame


class GameObject(ABC):
    """Base abstrak semua objek game.

    Koordinat/ukuran disimpan protected (`_x`, ...) sesuai UML (#) dan
    diekspos lewat property read-only — bukti Encapsulation.
    """

    def __init__(self, x=0, y=0, width=0, height=0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def update(self):
        pass
