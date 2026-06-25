import random
import re
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

IMAGE_NAME_MAP = {
    "TRUK_MBG": "TRUCK_MBG",
}


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
                front_path = os.path.join(IMAGE_PATH, "traps", "OKNUM_KORUPTOR.png")
                card = KoruptorCard(x, y, CARD_WIDTH, CARD_HEIGHT,
                                    front_path, back_path)
            elif card_type == "tercemar":
                front_path = os.path.join(IMAGE_PATH, "cards", "MAKANAN_TERCEMAR.png")
                card = TercemarCard(x, y, CARD_WIDTH, CARD_HEIGHT,
                                    front_path, back_path)
            else:
                base_name = re.sub(r'_\d+$', '', value)
                image_name = IMAGE_NAME_MAP.get(base_name, base_name)
                front_path = os.path.join(IMAGE_PATH, "cards", f"{image_name}.png")
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
            if card.rect.collidepoint(pos):
                return card
        return None

    def all_matched(self):
        for card in self._cards:
            if isinstance(card, MatchCard) and not card.is_matched:
                return False
        return True

    def update(self):
        for card in self._cards:
            card.update()

    def update_hover(self, pos, active):
        for card in self._cards:
            hot = (active and not card.is_matched and not card.is_flipped
                   and not card.is_animating and card.rect.collidepoint(pos))
            card.set_hover(hot)

    def draw(self, screen):
        for card in self._cards:
            card.draw(screen)
