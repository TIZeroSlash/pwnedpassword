### **README - Password Pwnage Checker**

---

### **Deskripsi Proyek**
Proyek ini adalah aplikasi web yang memungkinkan pengguna untuk memeriksa apakah sebuah password pernah ditemukan dalam pelanggaran data sebelumnya. Aplikasi ini terintegrasi dengan **Pwned Passwords API** untuk memberikan informasi tentang jumlah pelanggaran yang melibatkan password yang dimasukkan.

---

### **Fitur Utama**
1. **Pengecekan Password**:
   - Memeriksa apakah password telah ditemukan dalam pelanggaran data sebelumnya.
   - Menampilkan jumlah pelanggaran di mana password tersebut muncul.
2. **Penyimpanan Riwayat**:
   - Menyimpan hash password yang dicek dan jumlah pelanggaran ke database.
   - Menampilkan riwayat pengecekan password dalam antarmuka web.
3. **API untuk Riwayat Pengecekan**:
   - Endpoint untuk mendapatkan riwayat pengecekan dalam format JSON.

---

### **Alur Logika**
1. **Input Password**:
   - Pengguna memasukkan password melalui form di halaman utama.
2. **Pengecekan API**:
   - Password di-hash menggunakan algoritma **SHA-1**.
   - Prefix hash dikirim ke **Pwned Passwords API** untuk mendapatkan daftar hash dengan pelanggaran yang cocok.
   - Sisa hash diperiksa terhadap hasil API untuk menentukan jumlah pelanggaran.
3. **Simpan dan Tampilkan**:
   - Jika password sudah pernah dicek, data diambil dari database.
   - Jika belum, hasil pengecekan disimpan ke database.
   - Tampilkan hasil dan riwayat pengecekan di halaman utama.

---

### **Struktur File**
```
.
├── app.py                 # Main Flask application
├── .env                   # Environment variables (Google API Key)
├── templates/
│   └── index.html         # HTML template untuk halaman utama
├── static/
│   └── style.css          # Style untuk aplikasi
└── requirements.txt       # Dependency Python
└── uwsgi.py       # Running production
```

### **Cara Menggunakan**
1. **Setup Environment**:
   - Buat file `.env` di direktori root dengan isi:
     ```
     DATABASE_URI=mysql+pymysql://username:password@localhost/db_name
     ```
     - Ganti `username`, `password`, dan `db_name` sesuai konfigurasi database Anda.

2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
3. **Jalankan Aplikasi**:
   ```
   python app.py
   ```
   Aplikasi akan berjalan di `http://127.0.0.1:5000/`.

4. **Deploy di Server (Optional)**:
   - Gunakan layanan seperti **PythonAnywhere** atau server VPS.
   - Pastikan DATABASE_URI sudah di set di .env dan dependencies sudah diinstall.

5. **Gunakan Aplikasi**:
   - Buka aplikasi di browser.
   - Masukkan password pada form input.
   - Dapatkan hasil pengecekan dan riwayat pengecekan.

---

### **Endpoint API**
1. **Halaman Utama** (`/`):
- **Method**: `GET` / `POST`
- **Fungsi**: Memasukkan password untuk pengecekan dan menampilkan hasil.
2. **API Check Password** (`/check_password`):
- **Method**: `POST`
- **Fungsi**: Menggunakan API untuk mengecek password secara langsung melalui request POST.
2. **API Riwayat Pengecekan** (`/history`):
- **Method**: `GET`
- **Fungsi**: Mengembalikan riwayat pengecekan password dalam format JSON.

---

### **Pesan Hasil**
1. **Password Terkena Pelanggaran**:
- Pesan: *"Oh no — pwned! This password has been seen X times before."*
- Penanganan: Informasikan jumlah pelanggaran kepada pengguna.
2. **Password Aman**:
- Pesan: *"Good news — no pwnage found! This password has not been seen in any breaches."*
- Penanganan: Informasikan bahwa password aman.
3. **Input Kosong**:
- Pesan: *"Please enter a password."*
- Penanganan: Tidak ada aksi selain menampilkan pesan.

---

### **Lisensi**
Proyek ini dilisensikan di bawah **GNU General Public License v3.0**. Anda dapat menggunakan, memodifikasi, dan mendistribusikan proyek ini sesuai ketentuan lisensi. Informasi lebih lanjut dapat ditemukan di [GNU Licenses](https://www.gnu.org/licenses/gpl-3.0.html).

---

### **Kontak**
Jika ada pertanyaan atau butuh bantuan, silakan kunjungi profil saya:
[**Muhammad Andyk Maulana**](https://muhammadandykmaulana.github.io)
	
