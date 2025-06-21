import React, { useState } from "react";
import { login } from "../api";

type Props = { onLogin: (token: string, role: string) => void };

const LoginForm: React.FC<Props> = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login(email, password);
      onLogin(res.access_token, res.role);
    } catch (e) {
      setErr("Email atau password salah");
    }
  };

  return (
    <form onSubmit={submit} style={{
      background: "#fff",
      maxWidth: 360,
      margin: "0 auto",
      padding: 32,
      borderRadius: 16,
      boxShadow: "0 4px 12px #0001"
    }}>
      <h2 style={{textAlign:"center", color:"#2e7d32"}}>Login</h2>
      {err && <div style={{color:"red", marginBottom:8}}>{err}</div>}
      <div>
        <label>Email</label>
        <input type="email" value={email}
          onChange={e=>setEmail(e.target.value)} style={{width:"100%", padding:8, marginBottom:12}} />
      </div>
      <div>
        <label>Password</label>
        <input type="password" value={password}
          onChange={e=>setPassword(e.target.value)} style={{width:"100%", padding:8, marginBottom:18}} />
      </div>
      <button style={{
        background:"#2e7d32", color:"#fff", width:"100%",
        padding:10, border:"none", borderRadius:8, fontWeight:700
      }}>Login</button>
    </form>
  );
};

export default LoginForm;