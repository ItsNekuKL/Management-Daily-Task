"""
lihat_tugas.py — Menampilkan daftar semua tugas dalam format tabel terminal.
"""

from function.ui import cetak_tabel_tugas


def lihat_tugas(daftar_tugas: list) -> None:
    cetak_tabel_tugas(daftar_tugas)
