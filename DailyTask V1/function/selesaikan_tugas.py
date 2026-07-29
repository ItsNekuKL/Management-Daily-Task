"""
Menandai tugas sebagai selesai dan mencatat ke riwayat undo.
"""

import datetime
from function.ui import cetak_tabel_tugas, tampilkan_pesan


def selesaikan_tugas(daftar_tugas, riwayat):
    print(f"\n═══ SELESAIKAN TUGAS ═══")
    cetak_tabel_tugas(daftar_tugas)
    
    # cek apakah masih ada tugas yang belum selesai
    belum_selesai = [i for i, t in enumerate(daftar_tugas) if not t.get("selesai")]
    if not belum_selesai:
        tampilkan_pesan("Semua tugas sudah selesai!")
        return daftar_tugas, riwayat

    try:
        no = int(input(f"Nomor tugas yang diselesaikan : ").strip())
        index = no - 1

        if index < 0 or index >= len(daftar_tugas):
            raise ValueError
        
    except ValueError:
        tampilkan_pesan("Nomor tidak valid.")
        return daftar_tugas, riwayat

    tugas = daftar_tugas[index]
    if tugas.get("selesai"):
        tampilkan_pesan(f"Tugas '{tugas['nama']}' sudah selesai sebelumnya.")
        return daftar_tugas, riwayat

    # Simpan riwayat pekerjaan yg telah dilakukan
    riwayat.append({
        "aksi": "selesai",
        "index": index,
        "snapshot": dict(tugas),
    })

    sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    daftar_tugas[index]["selesai"] = True
    daftar_tugas[index]["waktu_selesai"] = sekarang

    tampilkan_pesan(f"Tugas '{tugas['nama']}' ditandai selesai!", "sukses")
    return daftar_tugas, riwayat
