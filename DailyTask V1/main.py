"""
    MANAJER TUGAS HARIAN
    dengan Fitur Undo & Excel Export  
"""

from function.lihat_tugas import lihat_tugas
from function.tambah_tugas import tambah_tugas
from function.selesaikan_tugas import selesaikan_tugas
from function.undo import undo_aksi
from function.ekspor_excel import ekspor_excel
from function.storage import muat_data, simpan_data
from function.ui import tampilkan_menu, tampilkan_header, tampilkan_pesan


def main():
    daftar_tugas, riwayat = muat_data()

    while True:
        tampilkan_header()
        pilihan = tampilkan_menu()

        if pilihan == "1":
            lihat_tugas(daftar_tugas)
        elif pilihan == "2":
            daftar_tugas, riwayat = tambah_tugas(daftar_tugas, riwayat)
            simpan_data(daftar_tugas, riwayat)
        elif pilihan == "3":
            daftar_tugas, riwayat = selesaikan_tugas(daftar_tugas, riwayat)
            simpan_data(daftar_tugas, riwayat)
        elif pilihan == "4":
            daftar_tugas, riwayat = undo_aksi(daftar_tugas, riwayat)
            simpan_data(daftar_tugas, riwayat)
        elif pilihan == "5":
            ekspor_excel(daftar_tugas)
        elif pilihan == "0":
            tampilkan_pesan("\nSampai jumpa! Data telah disimpan.")
            break
        else:
            tampilkan_pesan("Pilihan tidak valid. Coba lagi.")

        input("\n  Tekan ENTER untuk melanjutkan...")


if __name__ == "__main__":
    main()

