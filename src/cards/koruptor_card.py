from src.cards.trap_card import TrapCard
from src.config.constants import OKNUM_KORUPTOR, TRAP_COLORS


class KoruptorCard(TrapCard):

    def __init__(self, x, y, width, height,
                 front_image_path=None, back_image_path=None):
        super().__init__(x, y, width, height, OKNUM_KORUPTOR,
                         front_image_path, back_image_path,
                         TRAP_COLORS[OKNUM_KORUPTOR])

    def on_flip(self):
        return "GAME_OVER"
