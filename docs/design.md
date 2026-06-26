# DESIGN — MBG Memory Match

**Visual & UX Design Document**
Memory Matching Game bertema Program Makan Bergizi Gratis (MBG) · Python 3.13 + Pygame 2.6.1

> Pendamping [`PRD.md`](./PRD.md), [`UML.md`](./UML.md), [`requirment-system.md`](./requirment-system.md), [`STRUCTURE.md`](./STRUCTURE.md).
> PRD mengatur **aturan main** (angka, formula). Dokumen ini mengatur **tampilan & rasa** (warna, tipografi, layout, animasi) dan cara mewujudkannya di Pygame.

---

## 0. Arah Desain (Design Direction)

Satu kalimat: **estetika "soft pastel playful" ala referensi *Memoria* — kartu 3D membulat, panel kaca (glassmorphism), latar blob lembut — diisi konten dunia MBG.**

| Keputusan | Pilihan | Alasan |
|---|---|---|
| Estetika | Soft pastel + rounded 3D + glassmorphism (dari *Memoria*) | Ramah, kasual, cocok sesi 1–3 menit; sesuai persona pemain kasual/penilai |
| Konten | Aset & ikon **MBG** (bukan otak generik) | Tema wajib MBG; trap koruptor/tercemar adalah jualan utama |
| Grid | **Ikut PRD**: Easy 4×3 · Medium 4×4 · Hard 6×4 | Konsisten dengan 11 gambar match. Memoria 8×5 **ditolak** (butuh 19 pasang, di luar scope aset) |
| Window | 1000×700, target 60 FPS | Sesuai PRD §2 & §10 |
| Penamaan level | Boleh pakai rasa Memoria (Starter/Expert/Master) sebagai *label*, tapi tetap tampilkan grid PRD | Kompromi: identitas Memoria + aturan PRD |

> **Catatan satir:** semua karakter generik/fiktif (tikus berdasi, pemimpin, petugas gizi). Bukan tokoh nyata. Pertahankan nada main-main, bukan menyerang individu.

---

## 1. Design Tokens

Token = sumber kebenaran tunggal untuk warna/ukuran. **Semua angka di bawah masuk ke `src/config/constants.py`** (lihat §9). Komponen tidak boleh pakai hex liar di luar token.

### 1a. Palet Warna

Diangkat dari referensi Memoria, disesuaikan agar punya warna semantik MBG (hijau "sehat", merah "koruptor", olive "tercemar").

| Token | Hex | Pakai untuk |
|---|---|---|
| `BG_CREAM` | `#FBF4EA` | stop gradient latar — pojok kiri-atas (hangat) |
| `BG_ROSE` | `#F7E8EC` | stop gradient latar — tengah (merah muda lembut) |
| `BG_LAVENDER` | `#E9E0F6` | stop gradient latar — ungu |
| `BG_SKY` | `#DCEAF6` | stop gradient latar — pojok kanan-bawah (biru) |
| `BRAND_BLUE` | `#6E8FE6` | awal gradient logo/judul |
| `BRAND_PURPLE` | `#9A6FE0` | akhir gradient logo/judul, aksen ungu |
| `CARD_PEACH` | `#F4A97D` | muka belakang kartu (tint A) |
| `CARD_PEACH_EDGE` | `#EC9460` | sisi/tebal kartu peach (efek 3D) |
| `CARD_LAVENDER` | `#C3ADE6` | muka belakang kartu (tint B) |
| `CARD_LAV_EDGE` | `#AE92DC` | sisi/tebal kartu lavender |
| `SURFACE_WHITE` | `#FFFFFF` | kartu menu solid, panel skor |
| `GLASS_WHITE` | `rgba(255,255,255,0.55)` | panel kaca HUD |
| `GLASS_BORDER` | `rgba(255,255,255,0.70)` | garis tepi-highlight panel kaca |
| `SUCCESS_GREEN` | `#6FBF73` | kartu cocok, badge "sehat", progress |
| `SUCCESS_GLOW` | `#A6E0A8` | glow saat match |
| `SCORE_GOLD` | `#F6C45A` | ikon bintang skor |
| `DANGER_RED` | `#E5654E` | KORUPTOR, layar kalah, vignette |
| `TERCEMAR_OLIVE` | `#A9A23E` | flash kartu makanan tercemar (kesan "kotor") |
| `INK` | `#6E5A6B` | teks utama (plum keabu hangat) |
| `INK_MUTED` | `#9A8CA3` | teks sekunder, caption, label |
| `SHADOW` | `rgba(110,90,107,0.18)` | drop shadow lembut semua elemen |

**Aturan warna:**
- Latar **selalu** gradient diagonal 4-stop (cream → rose → lavender → sky), arah kiri-atas → kanan-bawah.
- Hindari hitam murni & putih murni untuk teks/garis. Teks = `INK`/`INK_MUTED`. Garis = putih semi-transparan.
- Hijau, merah, olive **hanya** untuk makna (sukses, koruptor, tercemar). Jangan dipakai dekoratif.

### 1b. Tipografi

Pasangan font rounded yang menggemakan logo Memoria. Keduanya open-source (OFL) → aman dibundel ke `assets/fonts/`.

| Peran | Font | Ukuran (px) | Berat | Pakai untuk |
|---|---|---|---|---|
| Display | **Fredoka** | 64 / 48 / 24 | SemiBold–Bold | Judul "MBG", status Game Over, judul panel |
| Body | **Nunito** | 18 | Regular/SemiBold | Teks isi, deskripsi |
| Data/HUD | **Nunito** | 40 | ExtraBold | Angka besar skor & timer |
| Caption | **Nunito** | 14 | SemiBold | Label "Score:", "Timer:", footer |
| Button | **Fredoka** | 22 | SemiBold | Teks tombol |

> Fallback wajib: jika file font hilang, `asset_loader` jatuh ke `pygame.font.SysFont(None, ...)` agar game tetap jalan (sesuai PRD §8 "graceful").

### 1c. Bentuk, Spasi, Bayangan

| Token | Nilai | Pakai |
|---|---|---|
| `RADIUS_CARD` | 20 px | sudut kartu main |
| `RADIUS_PANEL` | 28 px | sudut panel kaca / kartu menu |
| `RADIUS_PILL` | 999 px | tombol (kapsul penuh) |
| `RADIUS_SM` | 12 px | badge, chip kecil |
| `SPACE` | 4·8·12·16·24·32·48 | skala jarak (kelipatan 4) |
| `GAP_CARD` | 16 px | jarak antar kartu di board |
| `SHADOW_SOFT` | offset (0,6) blur 18, `SHADOW` | bayangan default |
| `SHADOW_LIFT` | offset (0,10) blur 26, `SHADOW` | elemen "terangkat" (hover/animasi) |

---

## 2. Sistem Layout (per Scene)

Semua scene memakai latar gradient + beberapa **blob** dekoratif (lingkaran besar blur) + partikel kecil (bintang/ikon MBG mengambang). Blob statis atau melayang sangat pelan (ambient).

### 2a. MenuScene

```
┌──────────────────────────────────────────────────────────────┐
│  MBG MEMORY MATCH (logo gradient)                  [profil]   │
│                                                               │
│  Siap mencocokkan          ┌────────┐ ┌────────┐ ┌────────┐  │
│  paket bergizi?            │ ikon   │ │POPULER │ │ ikon   │  │
│                            │ Easy   │ │ ikon   │ │ Hard   │  │
│  [ Tema: MBG ]            │  4×3   │ │Medium  │ │  6×4   │  │
│                            │[Play]  │ │  4×4   │ │[Play]  │  │
│                            └────────┘ │[Play]  │ └────────┘  │
│                                       └────────┘             │
│                            ┌─────────────────┐ ┌──────────┐  │
│                            │ Cara Main (tips) │ │ Skor     │  │
│                            └─────────────────┘ │ Terakhir │  │
│  © MBG Memory Match                            └──────────┘  │
└──────────────────────────────────────────────────────────────┘
```

- **Hero kiri:** judul gradient besar (Fredoka 64) + 1 kalimat ajakan + chip tema. Inilah "thesis" halaman.
- **3 kartu level** (putih solid, `RADIUS_PANEL`, `SHADOW_SOFT`): ikon MBG di atas, nama level, **grid PRD** sebagai subjudul, tombol Play pill bergradient. Kartu tengah (Medium) sedikit lebih tinggi + badge **"POPULER"** (meniru komposisi Memoria).
- **Tombol Play** tiap level beda gradient: Easy biru, Medium peach→merah, Hard ungu.
- **Panel bawah opsional:** "Cara Main" (3 bullet) + "Skor Terakhir" (sesi berjalan saja — *non-goal* save persisten).

> Penyederhanaan vs Memoria: tidak ada notifikasi/avatar fungsional, tidak ada leaderboard server. Profil/skor hanya hiasan sesi.

### 2b. GameScene

```
┌──────────────────────────────────────────────────────────────┐
│  MBG MEMORY MATCH         ┌──┬──┬──┬──┬──┬──┐      ┌────────┐ │
│ ╭───────────────╮         │  │  │  │  │  │  │      │ ⏸ Pause│ │
│ │ ⭐ Skor        │         ├──┼──┼──┼──┼──┼──┤      ├────────┤ │
│ │    120         │         │  │  │  │  │  │  │      │ ⚙ Set  │ │
│ │ 🃏 Pasangan    │         ├──┼──┼──┼──┼──┼──┤      └────────┘ │
│ │    3 / 11      │         │  │  │  │  │  │  │                 │
│ │ ⏱ Waktu        │         ├──┼──┼──┼──┼──┼──┤                 │
│ │    00:48       │         │  │  │  │  │  │  │                 │
│ ╰───────────────╯         └──┴──┴──┴──┴──┴──┘                 │
│   (panel kaca)              (board, auto-grid)    (pill kanan) │
└──────────────────────────────────────────────────────────────┘
```

- **Panel HUD kiri (glassmorphism):** 3 baris — Skor (ikon bintang gold), Pasangan x/total (ikon kartu), Waktu mm:ss (ikon jam). Label `INK_MUTED` 14px, angka Nunito ExtraBold 40px `INK`.
- **Board tengah/kanan:** `Board` menghitung ukuran & posisi kartu otomatis agar grid pas di area board (sesuai PRD F4 "layout auto"). Target kartu ±110–130px, `GAP_CARD` 16px. Board ter-*center* dalam area kanannya.
- **Pill kanan-atas:** tombol bulat Pause + Settings (gaya Memoria). Pause membekukan timer + meredupkan board (overlay).
- Timer **berubah warna** saat genting: `INK` → `DANGER_RED` ketika ≤10 detik (plus denyut halus).

### 2c. GameOverScene

```
┌──────────────────────────────────────────────────────────────┐
│                                                               │
│                 ╭───────────────────────────╮                 │
│                 │        ✦ MENANG! ✦         │  ← status besar │
│                 │   (atau "Kena Koruptor!"   │                 │
│                 │    / "Waktu Habis")        │                 │
│                 │                            │                 │
│                 │   Skor      : 184          │                 │
│                 │   Waktu     : 01:12        │                 │
│                 │   Langkah   : 14           │                 │
│                 │                            │                 │
│                 │  [ Main Lagi ]  [ Menu ]   │                 │
│                 ╰───────────────────────────╯                 │
└──────────────────────────────────────────────────────────────┘
```

- Panel kaca center, status (Fredoka 48) **berwarna sesuai hasil**: Menang → `SUCCESS_GREEN`, Koruptor → `DANGER_RED`, Waktu Habis → `BRAND_PURPLE`.
- Statistik (Skor / Waktu terpakai / Langkah) rata kiri, Nunito.
- Dua tombol pill: **Main Lagi** (ke `GameScene` level sama) & **Menu**.
- Latar belakang efek sesuai hasil: Menang → konfeti/sparkle pelan; Koruptor → vignette merah; Waktu Habis → netral.

---

## 3. Anatomi Kartu (Signature Element)

Kartu adalah elemen paling diingat. Wajib terasa **3D, membulat, "bisa dipencet".**

### 3a. Tampak belakang (tertutup)

```
   ┌─────────────┐   ← muka atas (CARD_PEACH atau CARD_LAVENDER),
   │   ╭─────╮   │     gradient terang→sedikit gelap, RADIUS_CARD
   │   │ MBG │   │   ← ikon emboss (logo/garpu-sendok) di tengah,
   │   ╰─────╯   │     dibuat dari dua bayangan (gelap + terang)
   └─────────────┘
    ▒▒▒▒▒▒▒▒▒▒▒▒▒    ← "tebal" kartu: rect lebih gelap (…_EDGE)
                       di-offset 4px ke bawah → kesan 3D
```

- **Tint belakang berselang-seling peach/lavender** mengikuti pola **papan catur posisi grid** — **bukan** berdasarkan nilai kartu. (Penting: kalau tint ikut nilai, pemain bisa curang. Dokumentasikan: tint = fungsi `(row+col) % 2`.)
- Ikon emboss sama di semua kartu (logo MBG / garpu-sendok). Tidak membocorkan identitas.

### 3b. Tampak depan (terbuka)

- Muka putih `SURFACE_WHITE`, `RADIUS_CARD`, ikon/gambar MBG di tengah, label kecil opsional.
- **Match (cocok):** border + glow `SUCCESS_GREEN`/`SUCCESS_GLOW`, denyut sekali, tetap terbuka.
- **Salah (tidak cocok):** redup + getar kecil, lalu flip kembali.

### 3c. Kartu jebakan (saat terbuka)

Tertutup: **identik** kartu lain (adil). Saat terbuka:

| Trap | Visual | Sound | Hasil |
|---|---|---|---|
| `KoruptorCard` (tikus berdasi) | Flash `DANGER_RED`, **screen shake**, vignette merah, ikon koruptor | `game_over`/`trap` | **GAME OVER instan** → GameOverScene("Kena Koruptor!") |
| `TercemarCard` (makanan tercemar) | Flash `TERCEMAR_OLIVE` di kartu itu, teks mengambang **"−15s  −10"**, ikon "kotor" | `trap_penalty` | Penalty (−15 detik, −10 skor, clamp 0), kartu **menutup lagi**, main lanjut |

> Pembeda dua trap = bukti **Polymorphism** (`on_flip()` beda perilaku). Visualnya harus jelas berbeda agar pemain paham konsekuensinya.

---

## 4. Spesifikasi Animasi (Motion)

PRD §11 menandai detail animasi masih *TBD*; ini usulan baseline (durasi @60 FPS). Semua sederhana, hemat performa, dan **hormati reduced-motion** (lihat §7).

| Animasi | Durasi | Easing | Catatan |
|---|---|---|---|
| Flip kartu | ~180 ms | ease-in-out | Squash sumbu-X (lebar → 0 → lebar); tukar gambar di titik tersempit (lebar≈0) |
| Match pulse | ~250 ms | ease-out | Scale 1.0→1.06→1.0 + glow hijau memudar |
| Wrong shake | ~200 ms | — | Geser ±4px horizontal 3×, lalu flip balik |
| Koruptor shake | ~400 ms | decay | Goyang seluruh board ±8px + vignette merah masuk |
| Tercemar float | ~700 ms | ease-out | Teks penalty naik + fade; kartu flip balik di akhir |
| Win sparkle | ~1.2 s loop | — | Partikel bintang lembut di panel hasil |
| Timer denyut (≤10s) | 1 s loop | sine | Angka timer membesar tipis + warna merah |
| Hover tombol | ~120 ms | ease-out | Naik 2px + `SHADOW_LIFT` |

**State animasi kartu** (selaras UML §4 / catatan implementasi): klik **diabaikan** saat `is_animating`, `is_matched`, atau sudah `is_flipped`. `GameScene` pakai state machine IDLE → FIRST_ANIMATING → WAITING_SECOND → SECOND_ANIMATING → SHOWING_RESULT.

---

## 5. Sound Design

Map sesuai PRD §8 (loader graceful — diam bila file hilang).

| Event | File (`assets/sounds/`) | Karakter |
|---|---|---|
| Flip kartu | `flip.wav` | klik lembut "pop" |
| Pasangan cocok | `match.wav` | bel naik ceria |
| Salah | `wrong.wav` (opsional) | nada turun pendek |
| Menang | `win.wav` | fanfare kecil |
| Koruptor (kalah) | `game_over.wav` | nada dramatis turun |
| Tercemar (penalty) | `trap_penalty.wav` | "splat"/dengung kotor |

> Sound dimainkan oleh `Card`/scene secara internal. Volume master di settings; hormati saat Pause (hentikan/mute).

---

## 6. Cookbook Rendering Pygame

Look pastel-glass ini "dibikin tangan". Resep ringkas (detail teknis menyusul saat implementasi `utils/`):

**Latar gradient 4-stop diagonal**
Pre-render **sekali** ke `Surface` seukuran window (jangan tiap frame): interpolasi linear cream→rose→lavender→sky sepanjang diagonal, simpan, lalu `blit` tiap frame. Blob = lingkaran besar warna pastel di-`blur` (atau alpha rendah berlapis).

**Kartu 3D membulat**
1. Gambar rect "tebal" warna `…_EDGE` di-offset (0, +4), `RADIUS_CARD`.
2. Di atasnya, rect muka dengan gradient vertikal terang→sedikit gelap.
3. Highlight tipis putih-alpha di tepi atas, bayangan tipis di tepi bawah-dalam.
4. Drop shadow `SHADOW_SOFT` di belakang seluruhnya.
Gunakan `pygame.draw.rect(..., border_radius=RADIUS_CARD)`; untuk gradient pada bentuk membulat, gambar gradient ke surface lalu mask dengan rounded-rect alpha.

**Panel kaca (glassmorphism)**
Pendekatan praktis: ambil potongan latar di area panel → `blur` ringan → tumpuk `Surface` putih `alpha≈140` rounded → garis tepi `GLASS_BORDER` 1–2px → `SHADOW_SOFT`. (Blur sekali saat layout, bukan tiap frame.)

**Teks gradient (judul)**
Render teks ke surface, buat surface gradient `BRAND_BLUE→BRAND_PURPLE`, pakai teks sebagai mask (`BLEND_RGBA_MULT`/per-pixel alpha).

**Tombol pill**
Rounded penuh (`RADIUS_PILL`), isi gradient, teks Fredoka tengah, hover naik + `SHADOW_LIFT`, pressed turun 1px.

> Aturan performa (PRD §10, 60 FPS): pra-render semua yang statis (latar, panel kaca, muka kartu). Per-frame hanya menggambar ulang yang berubah (animasi). Hindari blur/gradient di dalam game loop.

---

## 7. Aksesibilitas & Robustness

- **Reduced motion:** sediakan toggle (settings). Saat aktif: matikan screen-shake & sparkle, perpendek/transisikan flip jadi cut, denyut timer jadi statis. Game tetap penuh fungsi.
- **Kontras teks:** `INK` di atas latar terang & panel kaca harus terbaca; jangan taruh teks di atas blob paling jenuh.
- **Target klik:** kartu ≥100px, tombol pill tinggi ≥44px.
- **Feedback bukan hanya warna:** match = warna **+** denyut **+** sound; trap = warna **+** ikon **+** sound (tidak mengandalkan warna saja).
- **Input robust** (PRD §10): klik pada kartu `matched`/animasi diabaikan; klik di luar board diabaikan.
- **Graceful assets:** gambar hilang → kotak warna + label teks; sound hilang → diam; font hilang → SysFont.

---

## 8. Aset Visual (selaras STRUCTURE.md & PRD §8)

```
assets/images/
  cards/      ≥11 gambar match unik (paket_makanan_1.png, truk_mbg_1.png,
              anak_sekolah_1.png, pak_pemimpin_1.png, petugas_gizi_1.png, … varian)
  traps/      koruptor.png (tikus berdasi), makanan_tercemar.png
  card_back.png   ikon emboss MBG (1 file, tint diberi via kode)
assets/sounds/   flip, match, wrong, win, game_over, trap_penalty
assets/fonts/    Fredoka-SemiBold.ttf, Nunito-Regular.ttf, Nunito-ExtraBold.ttf
```

**Pedoman ilustrasi:** gaya 3D clay/soft-render seperti Memoria (volume membulat, highlight lembut), palet menyatu dengan token, latar transparan (PNG), satu gaya garis konsisten. Trap dibuat secara **visual berbeda jelas** dari match (koruptor = gelap/merah berdasi, tercemar = hijau-olive berlalat) — tapi **hanya terlihat saat terbuka**.

---

## 9. Token → Kode (`config/constants.py`)

Cuplikan agar desain & implementasi tidak menyimpang. Lengkapnya saat coding.

```python
# ---- Window ----
WIDTH, HEIGHT, FPS = 1000, 700, 60

# ---- Warna (RGB) ----
BG_STOPS      = [(251,244,234), (247,232,236), (233,224,246), (220,234,246)]  # cream→rose→lavender→sky
BRAND_BLUE    = (110,143,230)
BRAND_PURPLE  = (154,111,224)
CARD_PEACH    = (244,169,125);  CARD_PEACH_EDGE = (236,148, 96)
CARD_LAVENDER = (195,173,230);  CARD_LAV_EDGE   = (174,146,220)
SURFACE_WHITE = (255,255,255)
SUCCESS_GREEN = (111,191,115);  SUCCESS_GLOW    = (166,224,168)
SCORE_GOLD    = (246,196, 90)
DANGER_RED    = (229,101, 78)
TERCEMAR_OLIVE= (169,162, 62)
INK           = (110, 90,107);  INK_MUTED       = (154,140,163)

# ---- Bentuk ----
RADIUS_CARD, RADIUS_PANEL, RADIUS_PILL, RADIUS_SM = 20, 28, 999, 12
GAP_CARD = 16
SPACE = (4, 8, 12, 16, 24, 32, 48)

# ---- Font (path + ukuran) ----
FONT_DISPLAY = "assets/fonts/Fredoka-SemiBold.ttf"
FONT_BODY    = "assets/fonts/Nunito-Regular.ttf"
FONT_DATA    = "assets/fonts/Nunito-ExtraBold.ttf"
SIZE = {"title":64, "h1":48, "h2":24, "body":18, "data":40, "caption":14, "button":22}
```


---

## 10. Open Items (desain)

- [ ] Final palet ilustrasi per kategori (warna dominan tiap match agar mudah dibedakan saat terbuka).
- [ ] Bentuk ikon emboss `card_back` (logo MBG vs garpu-sendok vs sun-ray).
- [ ] Detail easing flip final (PRD §11) — angka di §4 masih baseline, *tuning* setelah playtest.
- [ ] Apakah panel "Skor Terakhir" di menu dipertahankan (sesi-only) atau dibuang demi kebersihan.
- [ ] Aset font final: konfirmasi Fredoka + Nunito vs alternatif (Baloo 2 / Quicksand).

---

*Dokumen desain; cetak biru tampilan & rasa. Angka tampilan bisa di-tuning saat implementasi selama token & arah visual tetap konsisten dengan PRD/UML/STRUCTURE.*