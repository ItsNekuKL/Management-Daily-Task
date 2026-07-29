"""
Menambahkan tugas baru ke daftar dan mencatat ke riwayat undo.
"""

import datetime
from function.ui import tampilkan_pesan


def tambah_tugas(daftar_tugas, riwayat):
    print(f"\n═══ TAMBAH TUGAS BARU ═══")

    nama = input(f"Nama tugas : ").strip()
    if not nama:
        tampilkan_pesan("Nama tugas tidak boleh kosong.", "error")
        return daftar_tugas, riwayat

    sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    newtask = {
        "nama": nama,
        "selesai": False,
        "waktu_dibuat": sekarang,
        "waktu_selesai": "-",
    }

    daftar_tugas.append(newtask)

    # Simpan snapshot ke riwayat undo
    riwayat.append({
        "aksi":   "tambah",
        "index": len(daftar_tugas) - 1,
    })

    tampilkan_pesan(f"Tugas '{nama}' berhasil ditambahkan!")
    return daftar_tugas, riwayat
