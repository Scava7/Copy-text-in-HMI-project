import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog
from Open_File_tkinker import select_file

# Seleziona il file
excel_file = select_file()
if not excel_file:
    print("Nessun file selezionato. Uscita...")
    exit()

# Nome del database SQLite
db_file = "SW_Support.sqlite"

# Carica il file Excel
xls = pd.ExcelFile(excel_file)

# Connessione a SQLite
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Loop attraverso i fogli e crea una tabella per ciascuno
for sheet_name in xls.sheet_names:
    # Legge i dati del foglio e forza tutte le colonne a essere trattate come dati
    df = xls.parse(sheet_name, index_col=None)

    # Se la colonna "N" esiste, convertirla in intero
    if "N" in df.columns:
        df["N"] = pd.to_numeric(df["N"], errors="coerce")  # Converte in numero, ignorando errori


    # Scrive i dati nel database (crea automaticamente le tabelle)
    df.to_sql(sheet_name, conn, if_exists="replace", index=False)

    print(f"Tabella '{sheet_name}' creata con successo!")

# Chiude la connessione
conn.close()
print(f"Importazione completata! Database salvato in '{db_file}'.")
