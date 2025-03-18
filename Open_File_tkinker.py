import tkinter as tk
from tkinter import filedialog


# Funzione per selezionare il file Excel
def select_Excel():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale di Tkinter
    file_path = filedialog.askopenfilename(
        title="Seleziona il file Excel",
        filetypes=[("File Excel", "*.xlsx *.xls")]
    )
    return file_path


