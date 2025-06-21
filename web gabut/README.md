# Manajemen Rohis SMKN 2 Luwu Timur

Aplikasi manajemen anggota, absensi, keuangan, kultum, dan pengumuman untuk organisasi Rohis SMKN 2 Luwu Timur.

## Backend

1. Masuk ke folder `backend/`
2. Copy `.env.example` ke `.env` dan isi variabel SUPABASE_URL & SUPABASE_KEY
3. Install dependensi:
    ```
    pip install -r requirements.txt
    ```
4. Jalankan backend:
    ```
    uvicorn main:app --reload
    ```

## Frontend

1. Masuk ke folder `frontend/`
2. Install dependensi:
    ```
    npm install
    ```
3. Jalankan frontend:
    ```
    npm run dev
    ```
4. Buka browser ke http://localhost:5173

## Fitur

- Dua peran: **Admin** (bisa CRUD semua data dan atur peran), **Anggota** (akses terbatas)
- Manajemen anggota, absensi, kas, kultum, pengumuman
- Autentikasi JWT
- Desain nuansa islami

---

Aplikasi ini dapat dikembangkan dan dikustomisasi lebih lanjut sesuai kebutuhan organisasi.