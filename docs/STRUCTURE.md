# STRUCTURE — MBG Memory Match

Peta struktur folder & tanggung jawab tiap file. Pendamping [`PRD.md`](./PRD.md), [`UML.md`](./UML.md), dan [`requirment-system.md`](./requirment-system.md).

> Aturan: **1 class = 1 file**, nama file `snake_case`, nama class `PascalCase`.

---

## Tree Lengkap

```
mbg-memory-match/
├── assets/                       # resource game (gambar, sound, font)
│   ├── images/
│   │   ├── cards/                # ≥11 gambar match (paket_makanan_1.png, dst)
│   │   ├── traps/                # koruptor.png, makanan_tercemar.png
│   │   └── card_back.png         # punggung kartu (tertutup)
│   ├── sounds/                   # flip, match, win, game_over, trap
│   └── fonts/                    # font UI
│
├── docs/                         # dokumentasi perencanaan
│   ├── requirment-system.md      # brief & knowledge base
│   ├── PRD.md                    # spesifikasi konkret (angka, formula, aturan)
│   ├── UML.md                    # class + sequence + state diagram
│   └── STRUCTURE.md              # dokumen ini
│
├── src/
│   ├── __init__.py
│   ├── main.py                   # entry point: init pygame + game loop + SceneManager
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py          # nilai mati: warna, ukuran, FPS, value kartu
│   │   └── settings.py           # config difficulty + path asset
│   │
│   ├── cards/
│   │   ├── __init__.py
│   │   ├── card.py               # Card(ABC)
│   │   ├── match_card.py         # MatchCard
│   │   ├── trap_card.py          # TrapCard(ABC)
│   │   ├── koruptor_card.py      # KoruptorCard  -> instant game over
│   │   └── tercemar_card.py      # TercemarCard  -> penalty
│   │
│   ├── objects/
│   │   ├── __init__.py
│   │   ├── game_object.py        # GameObject(ABC)
│   │   ├── button.py             # Button
│   │   └── board.py              # Board (grid + list Card)
│   │
│   ├── managers/
│   │   ├── __init__.py
│   │   ├── scene_manager.py      # SceneManager (transisi scene)
│   │   ├── score_manager.py      # ScoreManager (skor + moves)
│   │   └── timer.py              # Timer (countdown mm:ss)
│   │
│   ├── scenes/
│   │   ├── __init__.py
│   │   ├── scene.py              # Scene(ABC)
│   │   ├── menu_scene.py         # MenuScene
│   │   ├── game_scene.py         # GameScene
│   │   └── game_over_scene.py    # GameOverScene
│   │
│   └── utils/
│       ├── __init__.py
│       └── asset_loader.py       # load gambar/sound + fallback aman
│
├── .gitignore
├── requirements.txt              # pygame==2.6.1
└── README.md
```

---

## Tanggung Jawab per File

### `src/`
| File | Isi | Class |
|---|---|---|
| `main.py` | Inisialisasi pygame, buat `SceneManager`, jalankan game loop (handle_event → update → draw), kelola FPS clock | — |

### `config/`
| File | Isi |
|---|---|
| `constants.py` | Warna RGB, ukuran window/kartu/margin, `FPS`, enum value kartu (`PAKET_MAKANAN`, `OKNUM_KORUPTOR`, …) |
| `settings.py` | Dict difficulty `{EASY/MEDIUM/HARD: {rows, cols, pairs, traps, time}}`, path folder `assets/` |

### `cards/`
| File | Class | Tanggung jawab |
|---|---|---|
| `card.py` | `Card(ABC)` | state `_is_flipped`/`_is_matched`, `flip()`, abstractmethod `on_flip(game)` |
| `match_card.py` | `MatchCard` | `on_flip()` → cek pasangan, simpan poin bila cocok |
| `trap_card.py` | `TrapCard(ABC)` | base trap, abstractmethod `on_flip(game)` |
| `koruptor_card.py` | `KoruptorCard` | `on_flip()` → trigger **GAME OVER** |
| `tercemar_card.py` | `TercemarCard` | `on_flip()` → **penalty** (−15s & −10 skor), tidak kalah |

### `objects/`
| File | Class | Tanggung jawab |
|---|---|---|
| `game_object.py` | `GameObject(ABC)` | posisi/ukuran, `get_rect()`, abstractmethod `draw`/`update` |
| `button.py` | `Button` | tombol UI klik-able dengan callback |
| `board.py` | `Board` | generate grid acak per difficulty, sisip 1 koruptor + 1 tercemar, simpan list `Card`, `all_matched()` |

### `managers/`
| File | Class | Tanggung jawab |
|---|---|---|
| `scene_manager.py` | `SceneManager` | simpan scene aktif, delegasi event/update/draw, `set_scene()` |
| `score_manager.py` | `ScoreManager` | `_score`/`_moves` private, `add`/`penalty`/`reset`, property read-only |
| `timer.py` | `Timer` | countdown delta-time, `is_expired()`, `format()` mm:ss, `subtract()` |

### `scenes/`
| File | Class | Tanggung jawab |
|---|---|---|
| `scene.py` | `Scene(ABC)` | abstractmethod `handle_event`/`update`/`draw` |
| `menu_scene.py` | `MenuScene` | judul, tombol Play/Quit, pilih level |
| `game_scene.py` | `GameScene` | komposisi `Board`+`ScoreManager`+`Timer`, logika flip, `check_win()`, `game_over()` |
| `game_over_scene.py` | `GameOverScene` | tampil hasil (status/skor/waktu/moves), tombol Restart & Menu |

### `utils/`
| File | Isi |
|---|---|
| `asset_loader.py` | Fungsi load gambar & sound dari `assets/`, dengan fallback (warna/teks) bila file hilang |

---

## Status Implementasi

| Legenda | Arti |
|---|---|
| 🟩 | File ada, sudah ada isi |
| 🟨 | File ada, **masih kosong** (perlu diisi) |
| ⬜ | Folder asset (perlu diisi resource) |

```
src/scenes/scene.py ............ 🟩 (Scene ABC sudah ada)
src/main.py .................... 🟨 (loop standalone, perlu rewrite ke SceneManager)
src/cards/*.py ................. 🟨
src/objects/*.py ............... 🟨
src/managers/*.py .............. 🟨
src/config/*.py ................ 🟨
src/utils/asset_loader.py ...... 🟨
assets/ ........................ ⬜ (belum ada resource)
```

> Semua `__init__.py` sengaja kosong (penanda package Python).

---

*Dokumen struktur; belum termasuk kode implementasi.*
