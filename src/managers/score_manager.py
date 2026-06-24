class ScoreManager:
    def __init__(self):
        self._score = 0
        self._moves = 0

    @property
    def score(self):
        return self._score

    @property
    def moves(self):
        return self._moves

    def add_score(self, points):
        self._score += points

    def add_move(self):
        self._moves += 1

    def reset(self):
        self._score = 0
        self._moves = 0