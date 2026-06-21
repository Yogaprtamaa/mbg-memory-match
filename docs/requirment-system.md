# MBG Memory Match

**Project Brief & Knowledge Base — Memory Matching Game (Python + Pygame)**

> Tema: Program Makan Bergizi Gratis (MBG) | Fokus: Implementasi OOP

---

## Overview

| | |
|---|---|
| **Engine** | Python 3.x + Pygame |
| **Tipe** | Tugas implementasi OOP |
| **Mini-game** | Purble Pairs (Memory Matching) |
| **Pilar OOP** | Encapsulation, Inheritance, Polymorphism, Abstraction + Composition |

## Deskripsi

Pemain membalik kartu untuk mencocokkan pasangan elemen program MBG (paket makanan bergizi, truk distribusi, anak sekolah, petugas gizi). Cocokkan semua pasangan sebelum waktu habis untuk menang.

**Twist gameplay:** ada **kartu jebakan** bertema oknum koruptor. Jika kartu ini terbuka, permainan langsung **GAME OVER**. Mekanik ini menambah elemen risiko sekaligus memperkuat polymorphism (kartu jebakan punya perilaku berbeda dari kartu pasangan).

---

## In Scope

- 1 mini-game memory matching bertema MBG
- Menu, gameplay, skor, level kesulitan, layar game over
- Feedback audio & visual (flip, match, win)
- Mekanik kartu jebakan (trap card)

## Out of Scope

- Mini-game lain (Comfy Cakes, Purble Shop)
- Multiplayer / online
- Save-load persisten & leaderboard server

---

## Daftar Kartu

| Kategori | Variable (kode) | Tema MBG | Fungsi |
|---|---|---|---|
| Match card | `PAKET_MAKANAN` | Paket makanan bergizi | Pasangan (poin) |
| Match card | `TRUK_MBG` | Truk distribusi MBG | Pasangan (poin) |
| Match card | `ANAK_SEKOLAH` | Anak sekolah penerima | Pasangan (poin) |
| Match card | `PAK_PEMIMPIN` | Mascot pemimpin (generik) | Pasangan (poin) |
| Match card | `PETUGAS_GIZI` | Petugas dapur / gizi (generik) | Pasangan (poin) |
| TRAP card | `MAKANAN_TERCEMAR` | Makanan tercemar | Terbuka = penalty (−15 detik & −10 skor), tidak langsung kalah |
| TRAP card | `OKNUM_KORUPTOR` | Tikus berdasi (fiktif) | Terbuka = GAME OVER |

> Catatan: `PAK_PEMIMPIN`, `PETUGAS_GIZI`, dan `OKNUM_KORUPTOR` adalah peran generik/fiktif — bukan tokoh nyata bernama asli.

---

## Arsitektur Class

- `GameObject(ABC)` → `Card(ABC)` → `MatchCard`, `TrapCard(ABC)` → `KoruptorCard` / `TercemarCard`, plus `Button`
- `Scene(ABC)` → `MenuScene`, `GameScene`, `GameOverScene`
- `Board` *has-a* list `Card` (campur match + trap)
- `GameScene` *has-a* `Board` + `ScoreManager` + `Timer`
- `SceneManager` kelola transisi: `MENU` → `PLAYING` → `GAME_OVER`
- Game over trigger: buka `TrapCard` **atau** waktu habis

---

## Pemetaan Pilar OOP

| Pilar | Lokasi Pembuktian | Kekuatan |
|---|---|---|
| **Encapsulation** | `Card._is_flipped` / `_is_matched`, `ScoreManager._score` — akses lewat property/method. | KUAT |
| **Inheritance** | `Card` & `Scene` punya turunan nyata (`MatchCard`/`TrapCard`, `Menu`/`Game`/`GameOver`). | KUAT |
| **Polymorphism** | `MatchCard.on_flip()` (cek pasangan) vs `TrapCard.on_flip()` (game over) — method sama, behavior beda. | KUAT |
| **Abstraction** | `Card(ABC)` & `Scene(ABC)` dengan `@abstractmethod` (`draw`, `update`, `handle_event`). | MEDIUM-KUAT |
| **Composition** | `Board` « `Card`, `GameScene` « `Board`/`Score`/`Timer` (relasi has-a). | KUAT |

---

## Fitur 1 — Main Menu / Launcher

*Pilar: Inheritance, Polymorphism*

- [ ] Bikin base class `Scene(ABC)`: abstractmethod `handle_event`, `update`, `draw`
- [ ] Bikin `SceneManager` (set/switch scene aktif)
- [ ] Implement `MenuScene` (judul MBG, tombol Play, Quit, pilih level)
- [ ] Navigasi Play → pindah ke `GameScene`

## Fitur 2 — Core Gameplay (Memory Match)

*Pilar: Encapsulation, Composition, Polymorphism*

- [ ] Bikin base `GameObject(ABC)` dan `Card(ABC)`
- [ ] Class `MatchCard` (state `is_flipped`, `is_matched`, value/asset)
- [ ] Class `TrapCard` (`OKNUM_KORUPTOR`) — `on_flip()` trigger game over
- [ ] Class `Board`: generate grid acak, sisip 1+ `TrapCard`, simpan list `Card`
- [ ] Logika flip 2 kartu: cocok simpan, tidak cocok balik lagi
- [ ] Deteksi menang: semua `MatchCard` matched

## Fitur 3 — Score & Timer System

*Pilar: Encapsulation*

- [ ] Class `ScoreManager` (`_score`, `_moves`, add/reset, property read-only)
- [ ] Class `Timer` (hitung waktu, format mm:ss)
- [ ] Update skor & moves tiap flip benar/salah
- [ ] Render skor + timer di `GameScene`

## Fitur 4 — Difficulty Levels

*Pilar: Polymorphism / konfigurasi*

- [ ] Definisi level: Easy 4x3, Medium 4x4, Hard 6x4
- [ ] `Board` terima parameter ukuran grid + jumlah trap
- [ ] UI pilih level di menu
- [ ] Layout kartu otomatis menyesuaikan ukuran grid

## Fitur 5 — Win / Game Over Screen

*Pilar: Inheritance*

- [ ] Implement `GameOverScene` (turunan `Scene`)
- [ ] Tampilkan hasil: skor, waktu, moves, status (menang / kena trap / waktu habis)
- [ ] Tombol Restart (ke `GameScene`) & Menu (ke `MenuScene`)
- [ ] Trigger pindah scene saat menang / buka `TrapCard` / timeout

## Fitur 6 — Sound & Visual Feedback

*Pilar: Composition*

- [ ] Load asset sound (flip, match, win, game over) & gambar kartu
- [ ] `Card` punya komponen animasi flip sederhana
- [ ] Play sound saat aksi (flip / match / win / trap)
- [ ] Feedback visual: highlight match, efek game over saat trap terbuka

---

*Dokumen ini adalah brief perencanaan (belum termasuk kode). Semua karakter bertema MBG menggunakan peran generik/fiktif.*