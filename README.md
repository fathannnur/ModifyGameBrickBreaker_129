# Block Breaker

## Deskripsi
Block Breaker adalah game sederhana yang dibuat menggunakan Python dan library Pygame. Pemain harus memantulkan bola menggunakan paddle untuk menghancurkan balok yang berada di bagian atas layar.

Game ini menggunakan tema luar angkasa dengan background bintang, berbagai warna balok, musik latar, dan efek suara.

## Penjelasan Program

### 1. Striker
Class `Striker` digunakan untuk membuat dan mengatur paddle. Paddle dapat digerakkan ke kiri dan kanan menggunakan tombol panah pada keyboard.

### 2. Block
Class `Block` digunakan untuk membuat balok. Setiap balok memiliki warna dan tingkat ketahanan yang berbeda. Balok akan menghilang setelah ketahanannya habis terkena bola.

### 3. Ball
Class `Ball` mengatur posisi dan pergerakan bola. Bola dapat memantul ketika mengenai dinding, bagian atas layar, paddle, atau balok.

### 4. Collision Checker
Fungsi `collisionChecker()` digunakan untuk memeriksa tabrakan antara bola dan objek permainan. Fungsi ini juga membantu menentukan apakah balok terkena bola.

### 5. Populate Blocks
Fungsi `populateBlocks()` digunakan untuk membuat balok dengan posisi dan warna yang dipilih secara acak.

### 6. Background
Fungsi `draw_background()` digunakan untuk menampilkan latar belakang bertema luar angkasa dengan animasi bintang.

### 7. Musik dan Efek Suara
Program menggunakan fungsi `create_music()` untuk membuat musik latar dan `make_sound()` untuk menghasilkan efek suara. Efek suara muncul ketika pemain memulai permainan, bola mengenai objek, balok hancur, dan permainan berakhir.

### 8. Main
Fungsi `main()` merupakan bagian utama yang menjalankan permainan. Bagian ini mengatur input keyboard, pergerakan bola dan paddle, tabrakan, skor, nyawa, serta tampilan permainan.

## Fitur Permainan
- Lima variasi warna balok dengan ketahanan berbeda.
- Background luar angkasa dengan animasi bintang.
- Musik latar dan efek suara.
- Sistem skor dan tiga nyawa.
- Tampilan awal permainan.
- Tampilan kemenangan dan Game Over.
- Fitur bermain ulang.

## Kontrol
| Tombol | Fungsi |
|---|---|
| SPACE | Memulai permainan
