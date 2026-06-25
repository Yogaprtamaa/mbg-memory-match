from abc import abstractmethod
from src.cards.card import Card


class TrapCard(Card):

    def __init__(self, x, y, width, height, value,
                 front_image_path=None, back_image_path=None,
                 front_color=(183, 28, 28)):
        super().__init__(x, y, width, height, value,
                         front_image_path, back_image_path, front_color)

    @abstractmethod
    def on_flip(self):
        pass
