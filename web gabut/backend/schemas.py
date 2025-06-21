from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class User(BaseModel):
    id: Optional[int]
    nama: str
    email: str
    password: Optional[str]
    role: str = "anggota"
    kelas: Optional[str]
    kontak: Optional[str]

class Anggota(BaseModel):
    id: Optional[int]
    nama: str
    kelas: str
    kontak: Optional[str]

class Absensi(BaseModel):
    id: Optional[int]
    anggota_id: int
    tanggal: date
    status: str

class Kas(BaseModel):
    id: Optional[int]
    tanggal: date
    jenis: str
    keterangan: str
    jumlah: int

class Kultum(BaseModel):
    id: Optional[int]
    tanggal: date
    tema: str
    pemateri: str
    ringkasan: Optional[str]

class Pengumuman(BaseModel):
    id: Optional[int]
    judul: str
    isi: str
    tanggal: datetime