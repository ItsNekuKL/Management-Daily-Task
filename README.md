# CLI Daily Task Tracker

Aplikasi Command Line Interface (CLI) berbasis Python untuk mencatat log pekerjaan harian secara cepat via terminal. Data yang terkumpul akan diekspor otomatis menjadi file Microsoft Excel (`.xlsx`) yang terstruktur untuk kebutuhan pelaporan.

---

## Tech Stack

| Teknologi | Peran / Fungsi |
| :--- | :--- |
| **Python 3.x** | Core engine aplikasi CLI |
| **Pandas** | Pemrosesan data log & manipulasi DataFrame |
| **OpenPyXL** | Eksekutor format dan output file Excel |
| **Argparse / Click** | Routing command dan argumen di terminal |

---

## Penjelasan Fitur

| Fitur | Command / Menu | Deskripsi Fungsional |
| :--- | :--- | :--- |
| **Quick Log** | `add` | Input detail pekerjaan (nama task, kategori, durasi, status) langsung dari CMD. |
| **Monitor Task** | `list` | Menampilkan tabel ringkasan pekerjaan hari ini di layar terminal. |
| **Export to Excel**| `export` | Mengkonversi dan merapikan data log menjadi spreadsheet Excel siap pakai. |
| **Local Storage** | - | Data disimpan sementara di `.csv` lokal tanpa butuh koneksi database luar. |

---

## Struktur Direktori

```text
daily-task-V1/
├── main.py
├── function/
│   └── ekspor_excel.py
│   └── Lihat_TUgas.py
│   └── selesaikan_tugas.py
│   └── storage.py
│   └── tambah_tugas.py
│   └── ui.py
│   └── undo.py
├── data_tugas.json
└── README.md

daily-task-V2/
├── main.py
├── function/
│   └── AddTask.py
│   └── HistoryStack.py
│   └── Validation.py
│   └── search.py
└── README.md
