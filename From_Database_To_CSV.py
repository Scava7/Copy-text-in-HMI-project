import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog
import csv  # Per gestire il salvataggio corretto del CSV
from Copy_Values import process_csv_same_lang, process_csv_events
#import numpy as np  # Import necessario per la funzione np.vectorize()

# Percorso fisso del database SQLite
DB_PATH = r"C:\Dev\Copy text in HMI project\SW_Support.sqlite"

# -----> Lettura del file CSV (FUORI dalla funzione) <-----
def select_file():
    """Mostra una finestra di dialogo per selezionare il file CSV."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Seleziona il file CSV",
        filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
    )
    return file_path


# -----> Legge il file CSV una sola volta <-----
csv_file = select_file()
if not csv_file:
    print("Nessun file CSV selezionato. Uscita...")
    exit()

df_csv = pd.read_csv(csv_file, encoding="utf-16", sep="\t", dtype=str)  # Mantiene i dati come stringhe

# -----> Connessione unica al database SQLite <-----
conn = sqlite3.connect(DB_PATH)

# -----> Esegue la funzione 4 volte con parametri diversi <-----
process_csv_same_lang(df_csv, conn, "PAR BOOL",    "DESCRIPTION",      "TextParamDescriptionBool")
process_csv_same_lang(df_csv, conn, "PAR INT",     "DESCRIPTION",      "TextParamDescriptionInt")
process_csv_same_lang(df_csv, conn, "PAR INT",     "MEASURMENT_UNIT",  "TextParamUniMeasureInt")
process_csv_events( df_csv, conn, "ALARMS",         "ENG", "ITA",       "TextAlarm")
process_csv_events( df_csv, conn, "WARNINGS",       "ENG", "ITA",       "TextWarning")


# -----> Chiude la connessione al database <-----
conn.close()

# -----> Salva il CSV modificato <-----
output_file_name_utf16 = csv_file.replace(".csv", "_modificato.csv")
df_csv.to_csv(output_file_name_utf16, index=False, encoding="utf-16", sep="\t", quoting=3, lineterminator="\r\n")


print(f"Operazione completata! Il file aggiornato è stato salvato")
