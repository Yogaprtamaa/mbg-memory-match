from config.constants import LEVEL_EASY, LEVEL_MEDIUM, LEVEL_HARD

DIFFICULTY_SETTINGS = {
    LEVEL_EASY: {
        "rows": 3,
        "cols": 4,
        "pairs": 5,      # 10 kartu match
        "traps": 2,      # 1 koruptor + 1 tercemar
        "time": 120       # detik
    },
    LEVEL_MEDIUM: {
        "rows": 4,
        "cols": 4,
        "pairs": 7,      # 14 kartu match
        "traps": 2,      # 1 koruptor + 1 tercemar
        "time": 90        # detik
    },
    LEVEL_HARD: {
        "rows": 4,
        "cols": 6,
        "pairs": 11,     # 22 kartu match
        "traps": 2,      # 1 koruptor + 1 tercemar
        "time": 60        # detik
    }
}