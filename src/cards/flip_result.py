from enum import Enum, auto


class FlipResult(Enum):
    """Hasil polymorphic dari Card.on_flip().

    Mengganti 'magic string' agar dispatch di GameScene type-safe.
    Setiap subclass Card mengembalikan salah satu nilai ini.
    """

    NORMAL = auto()      # MatchCard: tidak ada efek khusus, lanjut evaluasi pasangan
    GAME_OVER = auto()   # KoruptorCard: langsung kalah
    PENALTY = auto()     # TercemarCard: kurangi skor & waktu, tidak kalah
