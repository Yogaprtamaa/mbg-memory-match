from src.cards.card import Card
from src.cards.flip_result import FlipResult


class MatchCard(Card):

    def __init__(self, x, y, width, height, value,
                 front_image_path=None, back_image_path=None,
                 front_color=(76, 175, 80)):
        super().__init__(x, y, width, height, value,
                         front_image_path, back_image_path, front_color)

    def on_flip(self):
        return FlipResult.NORMAL
