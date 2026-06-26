import random
import re
import os

from src.cards.match_card import MatchCard
from src.cards.koruptor_card import KoruptorCard
from src.cards.tercemar_card import TercemarCard
from src.config.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    CARD_WIDTH, CARD_HEIGHT, CARD_MARGIN,
    WINDOW_MARGIN, HUD_PANEL_W, BOARD_TOP,
    MATCH_VALUES, CARD_FRONT_COLORS,
)
from src.config.settings import DIFFICULTY, IMAGE_PATH

IMAGE_NAME_MAP = {
    "TRUK_MBG": "TRUCK_MBG",
}

CARD_ASPECT = CARD_HEIGHT / CARD_WIDTH  # tinggi : lebar


class Board:

    def __init__(self, level):
        config = DIFFICULTY[level]
        self._rows = config["rows"]
        self._cols = config["cols"]
        self._total_pairs = config["pairs"]
        self._cards = []
        self._generate(config)

    # ---------- Layout (auto-grid dalam area kanan, design.md §2b) ----------
    def _card_size(self):
        area_w = WINDOW_WIDTH - WINDOW_MARGIN * 2 - HUD_PANEL_W - 24
        area_h = WINDOW_HEIGHT - BOARD_TOP - WINDOW_MARGIN
        w_by_width = (area_w - CARD_MARGIN * (self._cols - 1)) / self._cols
        w_by_height = ((area_h - CARD_MARGIN * (self._rows - 1)) / self._rows) / CARD_ASPECT
        w = min(w_by_width, w_by_height, CARD_WIDTH)
        w = max(72, int(w))
        h = int(w * CARD_ASPECT)
        return w, h

    def _calculate_positions(self, card_w, card_h):
        grid_w = self._cols * card_w + CARD_MARGIN * (self._cols - 1)
        grid_h = self._rows * card_h + CARD_MARGIN * (self._rows - 1)

        area_x = WINDOW_MARGIN + HUD_PANEL_W + 24
        area_w = WINDOW_WIDTH - WINDOW_MARGIN - area_x
        area_h = WINDOW_HEIGHT - BOARD_TOP - WINDOW_MARGIN

        start_x = area_x + (area_w - grid_w) // 2
        start_y = BOARD_TOP + (area_h - grid_h) // 2

        positions = []
        for row in range(self._rows):
            for col in range(self._cols):
                x = start_x + col * (card_w + CARD_MARGIN)
                y = start_y + row * (card_h + CARD_MARGIN)
                positions.append((x, y, row, col))
        return positions

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

        card_w, card_h = self._card_size()
        positions = self._calculate_positions(card_w, card_h)
        back_path = os.path.join(IMAGE_PATH, "card_back.png")

        for idx, (x, y, row, col) in enumerate(positions):
            value, color, card_type = card_data[idx]

            if card_type == "koruptor":
                front_path = os.path.join(IMAGE_PATH, "traps", "OKNUM_KORUPTOR.png")
                card = KoruptorCard(x, y, card_w, card_h, front_path, back_path)
            elif card_type == "tercemar":
                front_path = os.path.join(IMAGE_PATH, "cards", "MAKANAN_TERCEMAR.png")
                card = TercemarCard(x, y, card_w, card_h, front_path, back_path)
            else:
                base_name = re.sub(r'_\d+$', '', value)
                image_name = IMAGE_NAME_MAP.get(base_name, base_name)
                front_path = os.path.join(IMAGE_PATH, "cards", f"{image_name}.png")
                card = MatchCard(x, y, card_w, card_h, value,
                                 front_path, back_path, color)

            # Tint belakang = papan catur posisi grid (BUKAN nilai → anti-curang).
            card.set_back_tint("peach" if (row + col) % 2 == 0 else "lavender")
            self._cards.append(card)

    # ---------- Query ----------
    def get_card_at(self, pos):
        for card in self._cards:
            if card.rect.collidepoint(pos):
                return card
        return None

    @property
    def total_pairs(self):
        return self._total_pairs

    @property
    def matched_pairs(self):
        matched = sum(1 for c in self._cards
                      if isinstance(c, MatchCard) and c.is_matched)
        return matched // 2

    def all_matched(self):
        for card in self._cards:
            if isinstance(card, MatchCard) and not card.is_matched:
                return False
        return True

    # ---------- Loop ----------
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
