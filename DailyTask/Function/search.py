import pandas as pd
import time

class PencarianMahasiswa:
    def __init__(self, df):
        """Konstruktor menerima DataFrame mahasiswa."""
        self.df = df

    def cari_berdasarkan_nama(self, nama_cari):
        """Mencari berdasarkan nama dan mengembalikan DataFrame hasil."""
        start_time = time.time()
        hasil = self.df[self.df['Nama'].str.lower() == nama_cari.lower()]
        end_time = time.time()
        waktu_pencarian = end_time - start_time
        if not hasil.empty:
            print(f"Data mahasiswa ditemukan (Waktu pencarian: {waktu_pencarian:.6f} detik):")
            print(hasil)
            return hasil
        else:
            print(f"Nama mahasiswa '{nama_cari}' tidak ditemukan. (Waktu pencarian: {waktu_pencarian:.6f} detik)")
            return None

    def cari_berdasarkan_nim(self, nim_cari):
        """Mencari berdasarkan NIM dan mengembalikan DataFrame hasil."""
        start_time = time.time()
        hasil = self.df[self.df['NIM'] == nim_cari]
        end_time = time.time()
        waktu_pencarian = end_time - start_time
        if not hasil.empty:
            print(f"Data mahasiswa ditemukan (Waktu pencarian: {waktu_pencarian:.6f} detik):")
            print(hasil)
            return hasil
        else:
            print(f"NIM '{nim_cari}' tidak ditemukan. (Waktu pencarian: {waktu_pencarian:.6f} detik)")
            return None