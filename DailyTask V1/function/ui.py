"""
Komponen antarmuka terminal: warna, header, menu, dan pesan.
"""

import os

# ── Kode warna ANSI
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"

BG_CYAN  = "\033[46m"
BG_BLUE  = "\033[44m"


def bersihkan_layar() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def tampilkan_header() -> None:
    bersihkan_layar()

    print()
    print(f"{'':^{55}}")
    print(f"{'MANAJER TUGAS HARIAN':^{55}}")
    print(f"{'':^{55}}")
    print()


def tampilkan_menu() -> str:
    menu_items = [
        ("1", "Lihat Semua Tugas"),
        ("2", "Tambah Tugas Baru"),
        ("3", "Selesaikan Tugas"),
        ("4", "Batalkan Aksi Terakhir (Undo)"),
        ("5", "Ekspor ke Excel"),
        ("0", "Keluar"),
    ]

    print(f"  {BOLD}{CYAN}{'─' * 46}{RESET}")
    for kode, label in menu_items:
        bullet = f"{YELLOW}[{kode}]{RESET}"
        print(f"   {bullet}  {WHITE}{label}{RESET}")
    print(f"  {BOLD}{CYAN}{'─' * 46}{RESET}")
    print()
    return input(f"  {BOLD}Pilih menu » {RESET}").strip()


def tampilkan_pesan(teks: str, tipe: str = "info") -> None:
    warna = {
        "sukses": GREEN,
        "error":  RED,
        "warning": YELLOW,
        "info":   CYAN,
    }.get(tipe, WHITE)
    print(f"\n  {warna}{BOLD}{teks}{RESET}")


def cetak_tabel_tugas(daftar_tugas: list) -> None:
    if not daftar_tugas:
        tampilkan_pesan("Belum ada tugas.", "warning")
        return

    col = {
        "no": 4,
        "nama": 28,
        "status": 9,
        "dibuat": 18,
        "selesai": 18,
    }

    def baris_pembatas(char="─"):
        bagian = [char * (v + 2) for v in col.values()]
        return f"  {GRAY}├{'┼'.join(bagian)}┤{RESET}"

    def header_tabel():
        h = (
            f" {BOLD}{CYAN}{'═══ DAFTAR TUGAS ═══'}{RESET}\n"
            f"  {GRAY}┌{'┬'.join('─' * (v + 2) for v in col.values())}┐{RESET}\n"
            f"  {GRAY}│{RESET}"
            f" {BOLD}{CYAN}{'No':>{col['no']}}{RESET} {GRAY}│{RESET}"
            f" {BOLD}{CYAN}{'Nama Tugas':<{col['nama']}}{RESET} {GRAY}│{RESET}"
            f" {BOLD}{CYAN}{'Status':^{col['status']}}{RESET} {GRAY}│{RESET}"
            f" {BOLD}{CYAN}{'Ditambahkan':<{col['dibuat']}}{RESET} {GRAY}│{RESET}"
            f" {BOLD}{CYAN}{'Diselesaikan':<{col['selesai']}}{RESET} {GRAY}│{RESET}"
        )
        return h

    print()
    print(header_tabel())
    print(baris_pembatas())

    for i, t in enumerate(daftar_tugas, 1):
        selesai    = t.get("selesai", False)
        warna_baris = GREEN if selesai else WHITE
        status_teks = f"{GREEN}✔ SELESAI{RESET}" if selesai else f"{YELLOW}○ BELUM  {RESET}"
        nama = t["nama"]
        if len(nama) > col["nama"] - 1:
            nama = nama[:col["nama"] - 2] + "…"

        dibuat  = t.get("waktu_dibuat", "-")[:16]
        selesai_waktu = t.get("waktu_selesai", "-")
        if selesai_waktu and selesai_waktu != "-":
            selesai_waktu = selesai_waktu[:16]

        print(
            f"  {GRAY}│{RESET}"
            f" {warna_baris}{i:>{col['no']}}{RESET} {GRAY}│{RESET}"
            f" {warna_baris}{nama:<{col['nama']}}{RESET} {GRAY}│{RESET}"
            f" {status_teks} {GRAY}│{RESET}"
            f" {DIM}{dibuat:<{col['dibuat']}}{RESET} {GRAY}│{RESET}"
            f" {DIM}{selesai_waktu:<{col['selesai']}}{RESET} {GRAY}│{RESET}"
        )

    print(f"  {GRAY}└{'┴'.join('─' * (v + 2) for v in col.values())}┘{RESET}")
    print(f"\n  {DIM}Total: {len(daftar_tugas)} tugas  |  "
          f"Selesai: {sum(1 for t in daftar_tugas if t.get('selesai'))}{RESET}")
    print()

