-- Tabel User (Admin & Anggota)
create table "user" (
  id serial primary key,
  nama text not null,
  email text not null unique,
  password_hash text not null,
  role text not null check (role in ('admin', 'anggota')),
  kelas text,
  kontak text
);

-- Tabel Anggota (bisa dipakai untuk tambahan data anggota jika ingin terpisah dari tabel user)
create table anggota (
  id serial primary key,
  nama text not null,
  kelas text not null,
  kontak text
);

-- Tabel Absensi
create table absensi (
  id serial primary key,
  anggota_id integer references anggota(id) on delete cascade,
  tanggal date not null,
  status text not null check (status in ('hadir', 'izin', 'sakit', 'alpha'))
);

-- Tabel Kas (Keuangan)
create table kas (
  id serial primary key,
  tanggal date not null,
  jenis text not null check (jenis in ('pemasukan', 'pengeluaran')),
  keterangan text,
  jumlah integer not null
);

-- Tabel Kultum
create table kultum (
  id serial primary key,
  tanggal date not null,
  tema text not null,
  pemateri text not null,
  ringkasan text
);

-- Tabel Pengumuman
create table pengumuman (
  id serial primary key,
  judul text not null,
  isi text not null,
  tanggal timestamptz not null default now()
);