<h1 align="cener">CLI Daily Task Tracker</h1>
<img src="https://github.com/ItsNekuKL/Management-Daily-Task/blob/main/IgnoreThis/4NO.jpg" width="100">

Aplikasi Command Line Interface (CLI) berbasis Python untuk mencatat log pekerjaan harian secara cepat via terminal. Data yang terkumpul akan diekspor otomatis menjadi file Microsoft Excel (`.xlsx`) yang terstruktur untuk kebutuhan pelaporan.

<h1 align="center">Tech Stack</h1>
<p align="center">
  <img src="https://img.shields.io/badge/python-111827?style=for-the-badge&logo=python&logoColor=ffdd54" alt="python" />
</p>

## Penjelasan Fitur

| Fitur | Command / Menu | Deskripsi Fungsional |
| :--- | :--- | :--- |
| **AddTask/Tambah_Tuagas** | `add` | Input detail pekerjaan (nama task, kategori, durasi, status) langsung dari CMD. |
| **HistoryStask/Lihat_tgas** | `list` | Menampilkan tabel ringkasan pekerjaan hari ini di layar terminal. |
| **Valifation/selesaikan_tgas** | `list` | Menyelesaikan tuagas yang sedang dikerjakan menjadi "selsai/done" dengenan menentukan tugasnya terlebih dahulu |
| **Export Excel**| `export` | Mengkonversi dan merapikan data log menjadi spreadsheet Excel siap pakai. |
| **Storage** | - | Data disimpan sementara di `.json` lokal tanpa butuh koneksi database luar. |

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
