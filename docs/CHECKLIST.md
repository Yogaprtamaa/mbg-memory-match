# CHECKLIST — MBG Memory Match

Progress implementasi per fitur. Tandai `[x]` jika sub-item sudah selesai.

---

## Urutan Prioritas Pengerjaan

Berdasarkan dependency antar komponen — kerjakan dari Phase 1 ke bawah.

```
Phase 1 (Fondasi)        Tidak bergantung file lain, semua fitur butuh ini
  │
Phase 2 (Kartu & Board)  Butuh Phase 1 untuk config & base class
  │
Phase 3 (Scene System)   Butuh Phase 2 agar GameScene bisa pakai Board/Card
  │
Phase 4 (Integrasi)      Menyambungkan semua scene + main loop
  │
Phase 5 (Polish)         Efek tambahan, bisa dikerjakan kapan saja setelah Phase 2
```

| Phase | Apa yang dikerjakan | Kenapa duluan |
|---|---|---|
| **1** | `constants.py`, `settings.py`, `GameObject(ABC)`, asset dasar | Semua file lain import dari sini — tanpa ini tidak bisa jalan |
| **2** | `MatchCard`, `TrapCard`, `KoruptorCard`, `TercemarCard`, `Board`, upgrade `ScoreManager` & `Timer` | Inti gameplay: tanpa kartu & board, tidak ada yang bisa dimainkan |
| **3** | `SceneManager`, `Button`, `MenuScene`, `GameScene`, `GameOverScene` | Menyatukan semua komponen ke layar yang bisa dinavigasi |
| **4** | Rewrite `main.py`, integrasi menang/kalah/restart | Game bisa dijalankan end-to-end |
| **5** | `asset_loader.py`, sound tambahan, efek visual, polish | Feedback & pengalaman bermain — tidak blocking gameplay |

---

## Phase 1 — Fondasi ⚡

> *Prioritas TERTINGGI. Kerjakan pertama.*

**Config (Fitur 4)**
- [x] `constants.py` — warna RGB, ukuran window (1000×700), ukuran kartu, margin, FPS, enum value kartu
- [x] `settings.py` — dict difficulty: Easy 4×3/120s, Medium 4×4/90s, Hard 6×4/60s (grid, pairs, traps, time)

**Base Class (Fitur 2)**
- [x] `GameObject(ABC)` — posisi/ukuran, `get_rect()`, abstract `draw`/`update`
- [x] `Card(ABC)` — state flip, animasi, `on_flip()` abstract *(sudah implementasi)*
- [x] `Scene(ABC)` — abstract `handle_event`/`update`/`draw` *(sudah implementasi)*

**Asset Minimal**
- [ ] 1 gambar punggung kartu (card back)
- [ ] Minimal 5 gambar match (cukup untuk Easy)
- [ ] 2 gambar trap (koruptor + makanan tercemar)

---

## Phase 2 — Kartu, Board & Scoring 🃏

> *Inti gameplay. Kerjakan setelah Phase 1 selesai.*

**Kartu Turunan (Fitur 2)**
- [x] `MatchCard` — `on_flip()` return None, pasangan dicek oleh GameScene
- [x] `TrapCard(ABC)` — base trap, abstract `on_flip()`
- [x] `KoruptorCard` — `on_flip()` return "GAME_OVER"
- [x] `TercemarCard` — `on_flip()` return "PENALTY"

**Board (Fitur 2)**
- [x] `Board` — generate grid acak per difficulty, sisip 1 koruptor + 1 tercemar
- [x] Layout kartu otomatis menyesuaikan ukuran grid

**Upgrade Score & Timer (Fitur 3)**
- [x] `ScoreManager` — `add_score()`, `penalty()` dengan clamp ke 0
- [x] `Timer` — countdown dengan `start()`, `tick()`, `subtract()`, `is_expired()`
- [x] Penalty skor: flip salah −2, trap tercemar −10
- [x] Skor di-clamp minimal 0 (tidak boleh negatif)
- [x] Timer countdown sesuai difficulty (bukan count-up)
- [x] Timer `subtract()` untuk penalty −15 detik
- [x] Bonus menang: `sisa_detik × 2`

---

## Phase 3 — Scene System 🖥️

> *Bangun layar-layar navigasi. Butuh Phase 2.*

**Scene Manager (Fitur 1)**
- [x] `SceneManager` — set/switch scene aktif, delegasi event/update/draw
- [x] `Button` — tombol UI klik-able dengan callback

**Menu (Fitur 1)**
- [x] `MenuScene` — judul MBG, tombol Play, Quit
- [x] UI pilih level (Easy / Medium / Hard)

**Gameplay Scene (Fitur 2)**
- [x] `GameScene` — komposisi Board + ScoreManager + Timer
- [x] Logika flip 2 kartu: cocok → tetap terbuka, tidak cocok → balik lagi
- [x] Render skor + timer + moves di layar
- [x] Deteksi menang: semua `MatchCard` matched

**Game Over (Fitur 5)**
- [ ] `GameOverScene` — turunan `Scene`
- [ ] Tampilkan status: Menang / Kena Koruptor / Waktu Habis
- [ ] Tampilkan statistik: skor akhir, waktu terpakai, moves
- [ ] Tombol Restart → `GameScene` ulang
- [ ] Tombol Menu → kembali ke `MenuScene`

---

## Phase 4 — Integrasi & Main Loop 🔗

> *Menyatukan semuanya. Game bisa jalan end-to-end.*

- [x] Rewrite `main.py` — init pygame + SceneManager + game loop (event → update → draw)
- [x] Navigasi: Menu → Play → Game → Win/Lose → kembali ke Menu *(sementara, nanti ke GameOverScene)*
- [x] Trigger game over: buka `KoruptorCard` / timer habis
- [x] Trigger menang: semua `MatchCard` matched → bonus skor

---

## Phase 5 — Sound, Visual & Polish ✨

> *Bisa dikerjakan kapan saja setelah Phase 2. Tidak blocking.*

**Asset Loader (Fitur 6)**
- [ ] `asset_loader.py` — load gambar & sound dengan fallback aman (warna/teks bila file hilang)

**Sound (Fitur 6)**
- [x] Sound flip *(sudah ada di Card)*
- [ ] Sound match (pasangan cocok)
- [ ] Sound win (menang)
- [ ] Sound game over (kalah)
- [ ] Sound trap penalty (buka makanan tercemar)

**Visual (Fitur 6)**
- [x] Animasi flip kartu (scale cosinus) *(sudah ada)*
- [ ] Highlight visual saat pasangan cocok
- [ ] Efek visual game over saat trap koruptor terbuka

**Asset Lengkap**
- [ ] Tambah gambar match hingga ≥11 unik (untuk Hard 11 pasang)
- [ ] Sound files lengkap: match.wav, win.wav, game_over.wav, trap.wav
- [ ] 1 font UI
 **update**
