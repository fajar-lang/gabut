import React from "react";

type Props = { anggota: any[] };

const AnggotaTable: React.FC<Props> = ({ anggota }) => (
  <table style={{
    width: "100%", background: "#fff", borderRadius:12,
    boxShadow: "0 2px 8px #0002", marginTop:16
  }}>
    <thead style={{background:"#b5e7a0"}}>
      <tr>
        <th style={{padding:8}}>Nama</th>
        <th>Kelas</th>
        <th>Kontak</th>
      </tr>
    </thead>
    <tbody>
      {anggota.map((a) => (
        <tr key={a.id}>
          <td style={{padding:8}}>{a.nama}</td>
          <td>{a.kelas}</td>
          <td>{a.kontak}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default AnggotaTable;