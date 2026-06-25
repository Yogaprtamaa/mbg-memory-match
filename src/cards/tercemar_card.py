from src.cards.trap_card import TrapCard
from src.config.constants import MAKANAN_TERCEMAR, TRAP_COLORS


class TercemarCard(TrapCard):

    def __init__(self, x, y, width, height,
                 front_image_path=None, back_image_path=None):
        super().__init__(x, y, width, height, MAKANAN_TERCEMAR,
                         front_image_path, back_image_path,
                         TRAP_COLORS[MAKANAN_TERCEMAR])

    def on_flip(self):
        return "PENALTY"
