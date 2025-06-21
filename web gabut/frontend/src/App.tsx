import React, { useEffect, useState } from "react";
import { login, setAuthToken, listAnggota } from "./api";
import LoginForm from "./components/LoginForm";
import AnggotaTable from "./components/AnggotaTable";

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم";

function App() {
  const [token, setToken] = useState<string|null>(localStorage.getItem("token"));
  const [role, setRole] = useState<string|null>(localStorage.getItem("role"));
  const [anggota, setAnggota] = useState<any[]>([]);

  useEffect(() => {
    setAuthToken(token);
    if (token && role === "admin") {
      listAnggota().then(setAnggota);
    }
  }, [token, role]);

  function handleLogin(token: string, role: string) {
    setToken(token);
    setRole(role);
    localStorage.setItem("token", token);
    localStorage.setItem("role", role);
  }

  function handleLogout() {
    setToken(null); setRole(null);
    localStorage.removeItem("token");
    localStorage.removeItem("role");
  }

  return (
    <div style={{
      fontFamily: "sans-serif",
      background: "#e7f6df",
      minHeight: "100vh",
    }}>
      <header style={{
        background: "#2e7d32",
        color: "#fff",
        padding: "1.5rem 0",
        textAlign: "center",
        marginBottom: "2rem",
        borderBottomLeftRadius: 36,
        borderBottomRightRadius: 36,
      }}>
        <div style={{fontSize:20, fontWeight:700, letterSpacing: 2}}>
          Manajemen Rohis SMKN 2 Luwu Timur
        </div>
        <div style={{
          fontFamily: "serif",
          fontSize:"1.5rem",
          marginTop: "0.5rem",
          letterSpacing: 3
        }}>
          {BISMILLAH}
        </div>
      </header>
      <main style={{maxWidth:800, margin:"0 auto"}}>
        {!token ? (
          <LoginForm onLogin={handleLogin} />
        ) : role === "admin" ? (
          <>
            <button style={{float:"right"}} onClick={handleLogout}>Logout</button>
            <h2>Daftar Anggota</h2>
            <AnggotaTable anggota={anggota} />
            {/* Tambahkan komponen AbsensiTable, KasTable, dsb, secara serupa */}
          </>
        ) : (
          <>
            <button style={{float:"right"}} onClick={handleLogout}>Logout</button>
            <p>Selamat datang anggota. Menu anggota bisa dikembangkan di sini.</p>
          </>
        )}
      </main>
      <footer style={{
        marginTop: 64,
        padding: "1.5rem 0",
        background: "#2e7d32",
        color: "#fff",
        textAlign: "center",
        borderTopLeftRadius: 36,
        borderTopRightRadius: 36,
      }}>
        &copy; {new Date().getFullYear()} Rohis SMKN 2 Luwu Timur
      </footer>
    </div>
  );
}

export default App;