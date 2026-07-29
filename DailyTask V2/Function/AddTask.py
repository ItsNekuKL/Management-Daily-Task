
import pandas as pd
from DailyTask.Function.HistoryStack import Generate
from HistoryStack import Undosys

class TodoManager:
    def __init__(self, filename="DataTodo.xlsx"):
        self.filename = filename
        self.riwayat = Undosys()
        try:
            self.tasks = pd.read_excel(self.filename).to_dict('records')
        except FileNotFoundError:
            self.tasks = []
            
    def svexcel(self):
        pd.DataFrame(self.tasks, columns=["NameTask", "Done"]).to_excel(self.filename, index=False)

    def tambah_tugas(self, nama):
        self.tasks.append({"NameTask": nama, "Done": False})
        self.riwayat.push({"act": "tambah"})
        self.svexcel()
        print("Tugas baru masuk excel.")
        
    def selesaikan_tugas(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["Done"] = True
            self.riwayat.push({"act": "Done", "index": index})
            self.svexcel()
            print("Tugas ditandai kelar, excel diupdate.")

    def batalkan_terakhir(self):
        last = self.riwayat.pop()
        if not last: return print("Riwayat kosong ngab.")
        
        if last["act"] == "tambah": 
            self.tasks.pop()
        elif last["act"] == "Done": 
            self.tasks[last["index"]]["Done"] = False
        
        self.svexcel()
        print("Undo sukses, excel balik ke sebelumnya.")
        
    def lihat_daftar(self):
        print("\n--- Daftar Tugas ---")
        for i, t in enumerate(self.tasks):
            status = "[v]" if t["Done"] else "[ ]"
            print(f"{i}. {status} {t['Nama Tugas']}")