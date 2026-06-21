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
        #_value: str
        #_is_flipped: bool
        #_is_matched: bool
        +is_flipped: bool
        +is_matched: bool
        +value: str
        +flip()
        +on_flip(game)*
        +draw(screen)
    }

    class Scene {
        <<abstract>>
        +handle_event(event)*
        +update()*
        +draw(screen)*
    }

    class TrapCard {
        <<abstract>>
        +on_flip(game)*
    }

    %% ---------- Card subclasses ----------
    class MatchCard {
        +on_flip(game)  : cek pasangan
    }
    class KoruptorCard {
        +on_flip(game)  : GAME OVER
    }
    class TercemarCard {
        +on_flip(game)  : -15s, -10 skor
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
        -rows: int
        -cols: int
        +generate(level)
        +get_card_at(pos) Card
        +all_matched() bool
        +draw(screen)
    }
    class ScoreManager {
        -_score: int
        -_moves: int
        +score: int
        +moves: int
        +add(points)
        +penalty(points)
        +add_move()
        +reset()
    }
    class Timer {
        -_total: int
        -_remaining: float
        +remaining: float
        +start(seconds)
        +tick(dt)
        +subtract(seconds)
        +is_expired() bool
        +format() str
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
| **Polymorphism** | `on_flip(game)` beda perilaku: `MatchCard` (cek pasangan) vs `KoruptorCard` (game over) vs `TercemarCard` (penalty) |
| **Encapsulation** | `_is_flipped`, `_is_matched`, `_score`, `_moves`, `_remaining` private + akses lewat property |
| **Composition** | `Board *-- Card`, `GameScene *-- Board/ScoreManager/Timer` (has-a) |

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
        GS->>C1: on_flip(game)
        Note over GS: simpan sebagai first_pick
    else sudah ada pilihan pertama
        GS->>C2: flip()
        GS->>C2: on_flip(game)
        GS->>SM: add_move()

        alt C2 adalah TRAP
            alt KoruptorCard
                C2-->>GS: game_over("trap")
            else TercemarCard
                C2->>T: subtract(15)
                C2->>SM: penalty(10)
                Note over GS: tutup kartu, lanjut main
            end
        else dua MatchCard
            alt value cocok
                GS->>SM: add(10)
                Note over C1,C2: is_matched = True
                GS->>GS: check_win()
            else tidak cocok
                GS->>SM: penalty(2)
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

- `on_flip(game)` menerima referensi `GameScene` agar kartu bisa memengaruhi `ScoreManager`/`Timer`/state (cara polymorphism memberi efek berbeda).
- `Board.generate(level)` membaca konfigurasi difficulty (§4 PRD): jumlah baris/kolom, jumlah pasangan, dan selalu menyisipkan 1 `KoruptorCard` + 1 `TercemarCard`, lalu mengacak posisi.
- `Timer.tick(dt)` dipanggil tiap frame dengan delta-time agar countdown independen dari FPS.
- Klik diabaikan bila kartu sudah `matched`, sudah `flipped`, atau saat 2 kartu sedang dievaluasi.

---

*Diagram ini cetak biru arsitektur; nama atribut/method bisa disesuaikan saat implementasi selama relasi & pilar OOP tetap terjaga.*
