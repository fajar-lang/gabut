import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List

from schemas import User, Anggota, Absensi, Kas, Kultum, Pengumuman
from supabase_client import fetch_data, insert_data, update_data, delete_data

SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Manajemen Rohis SMKN2 Lutim")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_user_by_email(email: str):
    users = await fetch_data("user", f"?email=eq.{email}")
    return users[0] if users else None

async def get_user(user_id: int):
    users = await fetch_data("user", f"?id=eq.{user_id}")
    return users[0] if users else None

async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if user and verify_password(password, user['password_hash']):
        return user
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

async def is_admin(current_user=Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user

# === Auth Endpoints ===
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

@app.post("/register", response_model=User)
async def register(user: User):
    if await get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = user.dict(exclude_none=True)
    user_data["password_hash"] = hash_password(user_data.pop("password"))
    if not user_data.get("role"):
        user_data["role"] = "anggota"
    result = await insert_data("user", user_data)
    return result

# === User/Admin Management ===
@app.get("/users", dependencies=[Depends(is_admin)], response_model=List[User])
async def list_users():
    return await fetch_data("user")

@app.post("/users", dependencies=[Depends(is_admin)], response_model=User)
async def add_user(user: User):
    if await get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = user.dict(exclude_none=True)
    user_data["password_hash"] = hash_password(user_data.pop("password"))
    result = await insert_data("user", user_data)
    return result

@app.patch("/users/{user_id}/role", dependencies=[Depends(is_admin)])
async def change_role(user_id: int, role: str):
    if role not in ["admin", "anggota"]:
        raise HTTPException(status_code=400, detail="Role invalid")
    await update_data("user", user_id, {"role": role})
    return {"msg": f"Role updated to {role}"}

@app.delete("/users/{user_id}", dependencies=[Depends(is_admin)])
async def delete_user(user_id: int):
    await delete_data("user", user_id)
    return {"msg": "User deleted"}

# === Anggota (CRUD) ===
@app.get("/anggota", dependencies=[Depends(is_admin)])
async def list_anggota():
    return await fetch_data("anggota")

@app.post("/anggota", dependencies=[Depends(is_admin)])
async def tambah_anggota(anggota: Anggota):
    return await insert_data("anggota", anggota.dict(exclude_none=True))

@app.patch("/anggota/{id}", dependencies=[Depends(is_admin)])
async def update_anggota(id: int, anggota: Anggota):
    await update_data("anggota", id, anggota.dict(exclude_unset=True))
    return {"msg": "Anggota updated"}

@app.delete("/anggota/{id}", dependencies=[Depends(is_admin)])
async def delete_anggota(id: int):
    await delete_data("anggota", id)
    return {"msg": "Anggota deleted"}

# === Absensi (CRUD) ===
@app.get("/absensi", dependencies=[Depends(is_admin)])
async def list_absensi():
    return await fetch_data("absensi")

@app.post("/absensi", dependencies=[Depends(is_admin)])
async def tambah_absensi(absensi: Absensi):
    return await insert_data("absensi", absensi.dict(exclude_none=True))

@app.patch("/absensi/{id}", dependencies=[Depends(is_admin)])
async def update_absensi(id: int, absensi: Absensi):
    await update_data("absensi", id, absensi.dict(exclude_unset=True))
    return {"msg": "Absensi updated"}

@app.delete("/absensi/{id}", dependencies=[Depends(is_admin)])
async def delete_absensi(id: int):
    await delete_data("absensi", id)
    return {"msg": "Absensi deleted"}

# === Kas/Keuangan (CRUD) ===
@app.get("/kas", dependencies=[Depends(is_admin)])
async def list_kas():
    return await fetch_data("kas")

@app.post("/kas", dependencies=[Depends(is_admin)])
async def tambah_kas(kas: Kas):
    return await insert_data("kas", kas.dict(exclude_none=True))

@app.patch("/kas/{id}", dependencies=[Depends(is_admin)])
async def update_kas(id: int, kas: Kas):
    await update_data("kas", id, kas.dict(exclude_unset=True))
    return {"msg": "Kas updated"}

@app.delete("/kas/{id}", dependencies=[Depends(is_admin)])
async def delete_kas(id: int):
    await delete_data("kas", id)
    return {"msg": "Kas deleted"}

# === Kultum (CRUD) ===
@app.get("/kultum", dependencies=[Depends(is_admin)])
async def list_kultum():
    return await fetch_data("kultum")

@app.post("/kultum", dependencies=[Depends(is_admin)])
async def tambah_kultum(kultum: Kultum):
    return await insert_data("kultum", kultum.dict(exclude_none=True))

@app.patch("/kultum/{id}", dependencies=[Depends(is_admin)])
async def update_kultum(id: int, kultum: Kultum):
    await update_data("kultum", id, kultum.dict(exclude_unset=True))
    return {"msg": "Kultum updated"}

@app.delete("/kultum/{id}", dependencies=[Depends(is_admin)])
async def delete_kultum(id: int):
    await delete_data("kultum", id)
    return {"msg": "Kultum deleted"}

# === Pengumuman (CRUD) ===
@app.get("/pengumuman")
async def list_pengumuman():
    return await fetch_data("pengumuman")

@app.post("/pengumuman", dependencies=[Depends(is_admin)])
async def tambah_pengumuman(pengumuman: Pengumuman):
    return await insert_data("pengumuman", pengumuman.dict(exclude_none=True))

@app.patch("/pengumuman/{id}", dependencies=[Depends(is_admin)])
async def update_pengumuman(id: int, pengumuman: Pengumuman):
    await update_data("pengumuman", id, pengumuman.dict(exclude_unset=True))
    return {"msg": "Pengumuman updated"}

@app.delete("/pengumuman/{id}", dependencies=[Depends(is_admin)])
async def delete_pengumuman(id: int):
    await delete_data("pengumuman", id)
    return {"msg": "Pengumuman deleted"}