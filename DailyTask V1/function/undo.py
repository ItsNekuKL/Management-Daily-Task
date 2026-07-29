"""
undo.py — Membatalkan aksi terakhir (tambah atau selesaikan tugas) menggunakan stack riwayat.
"""

from function.ui import tampilkan_pesan


def undo_aksi(daftar_tugas, riwayat):
    print(f"\n═══ BATALKAN AKSI TERAKHIR (UNDO) ═══")

    if not riwayat:
        tampilkan_pesan("Tidak ada aksi yang bisa dibatalkan.")
        return daftar_tugas, riwayat

    LastAct = riwayat.pop()
    tipe  = LastAct["aksi"]
    index = LastAct["index"]

    if tipe == "tambah":
        nama_tugas = daftar_tugas[index]["nama"]
        daftar_tugas.pop(index)
        tampilkan_pesan(f"Undo: Tugas '{nama_tugas}' dihapus dari daftar.")

    elif tipe == "selesai":
        snapshot = LastAct["snapshot"]
        nama_tugas = snapshot["nama"]
        daftar_tugas[index] = snapshot
        tampilkan_pesan(f"Undo: Status tugas '{nama_tugas}' dikembalikan ke BELUM SELESAI.")

    else:
        tampilkan_pesan("Tipe aksi tidak dikenal, undo dibatalkan.")

    return daftar_tugas, riwayat
