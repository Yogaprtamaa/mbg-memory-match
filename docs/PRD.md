# PRD — MBG Memory Match

**Product Requirements Document**
Memory Matching Game bertema Program Makan Bergizi Gratis (MBG)
Engine: Python 3.13 + Pygame 2.6.1 | Fokus: Implementasi OOP

> Dokumen turunan dari [`requirment-system.md`](./requirment-system.md). Berisi spesifikasi konkret (angka, formula, aturan) yang sebelumnya masih `TBD`. Diagram class/sequence/state ada di [`UML.md`](./UML.md).

---

## 1. Tujuan Produk

Membuat satu mini-game *memory matching* (gaya Purble Pairs) bertema MBG yang:
1. Menyenangkan & punya elemen risiko (kartu jebakan).
2. Menjadi sarana pembuktian 5 pilar OOP: Encapsulation, Inheritance, Polymorphism, Abstraction, Composition.

**Non-goal:** multiplayer, online, save persisten, leaderboard server, mini-game lain.

---

## 2. Persona & Konteks

| | |
|---|---|
| **Pengguna** | Pemain kasual / penilai tugas OOP |
| **Platform** | Desktop (Windows), window 1000×700 |
| **Sesi main** | 1–3 menit per ronde |
| **Input** | Mouse (klik kartu & tombol) |

---

## 3. Game Flow (high-level)

```
MENU ──Play──> PLAYING ──(menang | trap koruptor | timeout)──> GAME_OVER
  ^                                                                  |
  └──────────────────── Menu ───────────────────────────────────────┘
                         Restart ──> PLAYING
```

State transition detail ada di [UML.md → State Diagram](./UML.md#3-state-diagram).

---

## 4. Spesifikasi Difficulty

| Level | Grid | Slot | Pasangan (match) | Trap | Waktu |
|---|---|---|---|---|---|
| **Easy** | 4×3 | 12 | 5 pasang (10 kartu) | 2 (1 koruptor + 1 tercemar) | **120 detik** |
| **Medium** | 4×4 | 16 | 7 pasang (14 kartu) | 2 (1 koruptor + 1 tercemar) | **90 detik** |
| **Hard** | 6×4 | 24 | 11 pasang (22 kartu) | 2 (1 koruptor + 1 tercemar) | **60 detik** |

**Aturan komposisi:**
- Total kartu = (pasangan × 2) + jumlah trap = jumlah slot grid (selalu pas, genap + trap).
- Posisi semua kartu **diacak** tiap ronde.
- Trap selalu **1 `OKNUM_KORUPTOR` + 1 `MAKANAN_TERCEMAR`**.

> ⚠️ **Catatan asset:** Hard butuh 11 pasangan unik, sedangkan kategori tema MBG hanya 5. Maka tiap kategori boleh punya beberapa varian gambar (mis. `PAKET_MAKANAN_1`, `PAKET_MAKANAN_2`). Minimal **11 gambar match unik** harus disiapkan. Lihat §8.

---

## 5. Spesifikasi Kartu

| Kategori | Value (kode) | Tema | Efek saat terbuka |
|---|---|---|---|
| Match | `PAKET_MAKANAN` | Paket makanan bergizi | Cek pasangan → poin bila cocok |
| Match | `TRUK_MBG` | Truk distribusi | Cek pasangan → poin bila cocok |
| Match | `ANAK_SEKOLAH` | Anak sekolah penerima | Cek pasangan → poin bila cocok |
| Match | `PAK_PEMIMPIN` | Mascot pemimpin (generik) | Cek pasangan → poin bila cocok |
| Match | `PETUGAS_GIZI` | Petugas dapur/gizi (generik) | Cek pasangan → poin bila cocok |
| **TRAP** | `OKNUM_KORUPTOR` | Tikus berdasi (fiktif) | **Instant GAME OVER** |
| **TRAP** | `MAKANAN_TERCEMAR` | Makanan tercemar | **Penalty: −15 detik + −10 skor**, lalu kartu ditutup lagi (tidak langsung kalah) |

> Karakter generik/fiktif — bukan tokoh nyata.

**Perilaku trap (pembuktian Polymorphism):** kedua trap turunan `TrapCard` tapi `on_flip()` berbeda — `KoruptorCard` memicu game over, `TercemarCard` memicu penalty.

---

## 6. Scoring System

| Aksi | Efek skor | Catatan |
|---|---|---|
| Pasangan cocok | **+10** | per pasangan |
| Flip salah (2 kartu tidak cocok) | **−2** | per percobaan gagal |
| Buka `MAKANAN_TERCEMAR` | **−10 skor & −15 detik** | tidak game over |
| Menang (semua match terbuka) | **+ bonus** = `sisa_detik × 2` | hadiah kecepatan |

**Aturan:**
- Skor tidak boleh negatif → di-*clamp* minimal `0`.
- `moves` bertambah tiap kali sepasang kartu dievaluasi (cocok/tidak).
- Skor & moves disimpan di `ScoreManager` (private, akses via property read-only).

---

## 7. Win / Lose Conditions

| Hasil | Trigger | Layar |
|---|---|---|
| **MENANG** | Semua `MatchCard` berstatus `matched` | GameOver: "MENANG" |
| **KALAH (trap)** | `OKNUM_KORUPTOR` terbuka | GameOver: "Kena Koruptor!" |
| **KALAH (waktu)** | Timer mencapai 0 | GameOver: "Waktu Habis" |

Layar Game Over menampilkan: **status, skor akhir, waktu terpakai, moves**, + tombol **Restart** & **Menu**.

---

## 8. Asset Requirements

| Tipe | Item | Keterangan |
|---|---|---|
| Gambar | ≥11 gambar match unik | cukup untuk Hard (11 pasang) |
| Gambar | 2 gambar trap | koruptor + makanan tercemar |
| Gambar | 1 punggung kartu (back) | tampilan kartu tertutup |
| Sound | flip, match, win, game-over, trap-penalty | feedback audio |
| Font | 1 font UI | judul & teks |

Disimpan di folder `assets/`. Loader sebaiknya *graceful* (fallback ke warna/teks bila asset hilang).

---

## 9. Functional Requirements (mapping fitur)

| ID | Fitur | Acceptance singkat |
|---|---|---|
| F1 | Main Menu | Tombol Play, Quit, pilih level berfungsi & pindah scene |
| F2 | Core Gameplay | Flip 2 kartu, cocok→tetap terbuka, tidak→tertutup lagi; deteksi menang |
| F3 | Score & Timer | Skor/moves/timer ter-render & update sesuai §6; timer format mm:ss |
| F4 | Difficulty | 3 level sesuai §4; grid & trap menyesuaikan; layout auto |
| F5 | Win/Game Over | 3 kondisi §7; tombol Restart & Menu |
| F6 | Sound & Visual | Sound tiap aksi; animasi flip; highlight match; efek trap |

---

## 10. Non-Functional Requirements

- **Performa:** target 60 FPS pada window 1000×700.
- **Struktur kode:** mengikuti arsitektur class di [UML.md](./UML.md), pemisahan `cards/ config/ managers/ objects/ scenes/ utils/`.
- **Robust input:** klik di kartu yang sudah `matched`/sedang animasi diabaikan.
- **Kode terbaca:** penamaan konsisten, atribut private pakai prefix `_`.

---

## 11. Open Items / TBD tersisa

- [ ] Detail animasi flip (durasi, easing) — saat ini "sederhana", final menyusul implementasi.
- [ ] Daftar nama file asset final (gambar/sound) — menunggu aset disiapkan.
- [ ] Nilai bonus & penalty bisa di-*tuning* setelah playtest.

---

*PRD ini dokumen perencanaan; belum termasuk kode implementasi.*
