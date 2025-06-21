import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

async def fetch_data(table: str, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}{params}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

async def insert_data(table: str, data: dict):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json()[0] if r.json() else None

async def update_data(table: str, id: int, data: dict):
    url = f"{SUPABASE_URL}/rest/v1/{table}?id=eq.{id}"
    async with httpx.AsyncClient() as client:
        r = await client.patch(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json()

async def delete_data(table: str, id: int):
    url = f"{SUPABASE_URL}/rest/v1/{table}?id=eq.{id}"
    async with httpx.AsyncClient() as client:
        r = await client.delete(url, headers=headers)
        r.raise_for_status()
        return r.json()