"""
Menyimpan dan memuat data tugas dari file JSON lokal.
"""

import json
import os

DATA_FILE = "data_tugas.json"


def simpan_data(tugas, riwayat):
    data = {
        "tugas": tugas,
        "riwayat": riwayat
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def muat_data() -> tuple[list, list]:
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r") as f:
            File_Data = json.load(f)
        return File_Data.get("tugas", []), File_Data.get("riwayat", [])
    except json.JSONDecodeError:
        return

