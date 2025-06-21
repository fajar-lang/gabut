import axios from "axios";

const API_URL = "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
});

// Helper to add token to headers
export function setAuthToken(token: string|null) {
  if (token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete api.defaults.headers.common["Authorization"];
}

// Auth
export async function login(email: string, password: string) {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);
  const res = await api.post("/token", form);
  return res.data;
}

export async function register(data: any) {
  const res = await api.post("/register", data);
  return res.data;
}

// CRUD fetchers (example for anggota, duplicate for others)
export async function listAnggota() {
  const res = await api.get("/anggota");
  return res.data;
}