# UML — MBG Memory Match

Diagram arsitektur untuk implementasi OOP. Lihat juga [`PRD.md`](./PRD.md) dan [`requirment-system.md`](./requirment-system.md).

Diagram ditulis dengan **Mermaid** (render otomatis di GitHub/VS Code Markdown Preview Mermaid).

---

## 1. Class Diagram

```mermaid
classDiagram
    direction TB

    %% ---------- Abstract bases ----------
    class GameObject {
        <<abstract>>
        #x: int
        #y: int
        #width: int
        #height: int
        +draw(screen)* 
        +update()*
        +get_rect() Rect
    }

    class Card {
        <<abstract>>
        +rect: Rect
        +original_width: int
        +front_image: Surface
        +back_image: Surface
        +is_flipped: bool
        +is_animating: bool
        +flip_angle: int
        +flip_speed: int
        +sound_flip: Sound
        +flip()
        +update()
        +draw(surface)
        +on_flip()*
    }

    class Scene {
        <<abstract>>
        +handle_event(event)*
        +update()*
        +draw(screen)*
    }

    class TrapCard {
        <<abstract>>
        +on_flip()*
    }

    %% ---------- Card subclasses ----------
    class MatchCard {
        +on_flip()  : cek pasangan
    }
    class KoruptorCard {
        +on_flip()  : GAME OVER
    }
    class TercemarCard {
        +on_flip()  : -15s, -10 skor
    }

    %% ---------- Scene subclasses ----------
    class MenuScene {
        -buttons: list~Button~
        -selected_level
        +handle_event(event)
        +update()
        +draw(screen)
    }
    class GameScene {
        -board: Board
        -score: ScoreManager
        -timer: Timer
        -first_pick: Card
        +handle_event(event)
        +update()
        +draw(screen)
        +check_win() bool
        +game_over(reason)
    }
    class GameOverScene {
        -result: str
        -final_score: int
        -buttons: list~Button~
        +handle_event(event)
        +update()
        +draw(screen)
    }

    %% ---------- Other objects / managers ----------
    class Button {
        -text: str
        -callback
        +draw(screen)
        +update()
        +is_clicked(pos) bool
    }
    class Board {
        -_cards: list~Card~
        -_rows: int
        -_cols: int
        +get_card_at(pos) Card
        +all_matched() bool
        +update()
        +draw(screen)
    }
    class ScoreManager {
        -_score: int
        -_moves: int
        +score: int «property»
        +moves: int «property»
        +add_score(points)
        +penalty(points)
        +add_move()
        +reset()
    }
    class Timer {
        -_total: int
        -_remaining: float
        -_last_tick: int
        +remaining: float «property»
        +start()
        +tick()
        +subtract(seconds)
        +is_expired() bool
        +get_formatted_time() str
        +reset(total_seconds)
    }
    class SceneManager {
        -_current: Scene
        +set_scene(scene)
        +handle_event(event)
        +update()
        +draw(screen)
    }

    %% ---------- Relationships ----------
    GameObject <|-- Card
    GameObject <|-- Button
    Card <|-- MatchCard
    Card <|-- TrapCard
    TrapCard <|-- KoruptorCard
    TrapCard <|-- TercemarCard

    Scene <|-- MenuScene
    Scene <|-- GameScene
    Scene <|-- GameOverScene

    Board "1" o-- "*" Card : has-a
    GameScene "1" *-- "1" Board
    GameScene "1" *-- "1" ScoreManager
    GameScene "1" *-- "1" Timer
    MenuScene "1" o-- "*" Button
    GameOverScene "1" o-- "*" Button
    SceneManager "1" o-- "1" Scene : current
```

### Pemetaan Pilar OOP

| Pilar | Bukti di diagram |
|---|---|
| **Abstraction** | `GameObject`, `Card`, `Scene`, `TrapCard` = `<<abstract>>` dengan abstractmethod (`draw`, `update`, `on_flip`, ...) |
| **Inheritance** | `Card → MatchCard/TrapCard`, `TrapCard → Koruptor/Tercemar`, `Scene → Menu/Game/GameOver` |
| **Polymorphism** | `on_flip()` beda perilaku: `MatchCard` (cek pasangan) vs `KoruptorCard` (game over) vs `TercemarCard` (penalty) |
| **Encapsulation** | `_score`, `_moves` private + akses lewat `@property` read-only di `ScoreManager` |
| **Composition** | `Board o-- Card`, `GameScene *-- Board/ScoreManager/Timer` (has-a) |

---

## 2. Sequence Diagrams

### 2a. Flip Logic (membuka 2 kartu)

```mermaid
sequenceDiagram
    actor Player
    participant GS as GameScene
    participant B as Board
    participant C1 as Card (pick-1)
    participant C2 as Card (pick-2)
    participant SM as ScoreManager
    participant T as Timer

    Player->>GS: klik kartu
    GS->>B: get_card_at(pos)
    B-->>GS: Card

    alt belum ada pilihan pertama
        GS->>C1: flip()
        GS->>C1: on_flip()
        Note over GS: simpan sebagai first_pick
    else sudah ada pilihan pertama
        GS->>C2: flip()
        GS->>C2: on_flip()
        GS->>SM: add_move()

        alt C2 adalah TRAP
            alt KoruptorCard
                C2-->>GS: game_over("trap")
            else TercemarCard
                Note over GS: kurangi waktu & skor, tutup kartu, lanjut main
            end
        else dua MatchCard
            alt value cocok
                GS->>SM: add_score(10)
                Note over C1,C2: is_matched = True
                GS->>GS: check_win()
            else tidak cocok
                Note over C1,C2: flip kembali (tertutup)
            end
        end
        Note over GS: reset first_pick
    end
```

### 2b. Scene Transition (menu → main → game over)

```mermaid
sequenceDiagram
    actor Player
    participant Main as main loop
    participant SM as SceneManager
    participant Menu as MenuScene
    participant Game as GameScene
    participant Over as GameOverScene

    Player->>Menu: pilih level + klik Play
    Menu->>SM: set_scene(GameScene(level))
    SM->>Game: aktif

    loop tiap frame
        Main->>SM: handle_event / update / draw
        SM->>Game: delegasi
    end

    alt menang / trap koruptor / timeout
        Game->>SM: set_scene(GameOverScene(result))
        SM->>Over: aktif
    end

    alt klik Restart
        Over->>SM: set_scene(GameScene(level))
    else klik Menu
        Over->>SM: set_scene(MenuScene())
    end
```

---

## 3. State Diagram

### 3a. Game (scene-level)

```mermaid
stateDiagram-v2
    [*] --> MENU
    MENU --> PLAYING : klik Play
    PLAYING --> GAME_OVER : semua match (MENANG)
    PLAYING --> GAME_OVER : buka Koruptor (KALAH)
    PLAYING --> GAME_OVER : timer habis (KALAH)
    GAME_OVER --> PLAYING : Restart
    GAME_OVER --> MENU : Menu
    MENU --> [*] : Quit
```

### 3b. Card (state satu kartu)

```mermaid
stateDiagram-v2
    [*] --> FaceDown
    FaceDown --> FaceUp : flip() / on_flip()
    FaceUp --> FaceDown : tidak cocok / penalty tercemar
    FaceUp --> Matched : pasangan cocok
    Matched --> [*]
    note right of FaceUp
        Trap Koruptor dari FaceUp
        memicu GAME OVER (scene-level)
    end note
```

---

## 4. Catatan Implementasi

- `on_flip()` tanpa parameter — mengembalikan sinyal: `None` (MatchCard), `"GAME_OVER"` (KoruptorCard), `"PENALTY"` (TercemarCard). `GameScene` bertindak berdasarkan return value.
- `Card` menyimpan state animasi (`is_animating`, `flip_angle`, `flip_speed`) dan memainkan sound flip secara internal. Juga menyimpan `value` (identitas pasangan) dan `is_matched`.
- `Timer` menggunakan countdown: `start()` mulai, `tick()` kurangi `_remaining` per frame, `subtract(s)` untuk penalty, `is_expired()` cek habis.
- `ScoreManager.penalty(points)` mengurangi skor dengan clamp ke 0 (skor tidak boleh negatif).
- `Board` membaca konfigurasi difficulty saat konstruksi: membuat pasangan `MatchCard`, menyisipkan 1 `KoruptorCard` + 1 `TercemarCard`, mengacak posisi, dan menghitung layout grid otomatis.
- `GameScene` menggunakan state machine (IDLE → FIRST_ANIMATING → WAITING_SECOND → SECOND_ANIMATING → SHOWING_RESULT) untuk mengelola alur flip dan evaluasi.
- Klik diabaikan bila kartu sudah `matched`, sudah `flipped`, atau saat animasi berjalan (`is_animating`).

---

*Diagram ini cetak biru arsitektur; nama atribut/method bisa disesuaikan saat implementasi selama relasi & pilar OOP tetap terjaga.*
