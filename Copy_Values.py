import pandas as pd
import sqlite3
import csv  # Per gestire il salvataggio corretto del CSV
import numpy as np  # Import necessario per la funzione np.vectorize()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def check_table_exists(conn, table_name):
    """Verifica se una tabella esiste nel database."""
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    result = conn.execute(query).fetchone()
    if result is None:  # Restituisce True se la tabella esiste, False altrimenti  
        print(f"❌ ERRORE: La tabella '{table_name}' non esiste nel database.")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def process_csv_same_lang(df_csv, conn, db_table, db_column, search_value):
    """
    Funzione che:
    - Cerca le righe con `search_value` nella prima colonna di df_csv
    - Sostituisce la terza colonna con valori presi dalla tabella `db_table` e colonna `db_column` nel database
    - Copia lo stesso valore nelle tre colonne successive
    - Modifica direttamente `df_csv`

    :param df_csv: DataFrame con i dati del CSV
    :param conn: Connessione al database SQLite
    :param db_table: Nome della tabella nel database SQLite
    :param db_column: Nome della colonna da cui prendere i valori
    :param search_value: Valore da cercare nella prima colonna del CSV
    """
    
    check_table_exists(conn, db_table)

    """if not check_table_exists(conn, db_table):
        print(f"❌ ERRORE: La tabella '{db_table}' non esiste nel database.")
        return"""
    
    # Query per prendere i dati dalla tabella specificata
    query = f"SELECT {db_column} FROM '{db_table}'"
    df_db = pd.read_sql(query, conn)

    # Identifica le righe che contengono il valore di ricerca nella prima colonna
    mask = df_csv.iloc[:, 0] == search_value

    # Controlla se ci sono abbastanza valori nel database
    num_replacements = mask.sum()
    if num_replacements == 0:
        print(f"⚠️ ATTENZIONE: Nessuna riga trovata con '{search_value}' nel CSV.")
        return
    if num_replacements != len(df_db) :
        print(f"Attenzione: il numero di righe tra database e file .csv {search_value} / {db_table} è diverso.")
        return

    # Recupera i valori dal database
    values_from_db = df_db[db_column].values[:num_replacements]

    # Se la colonna è "MEASURMENT_UNIT", aggiunge le parentesi
    if db_column == "MEASURMENT_UNIT":
        value_to_copy = np.array(["[" + str(val) + "]" for val in values_from_db])  # List comprehension per aggiungere le parentesi
    else:
        value_to_copy = values_from_db  # Usa direttamente i valori senza modificarli

    # Sostituisce i valori nella terza colonna delle righe corrispondenti
    df_csv.loc[mask, df_csv.columns[2]] = value_to_copy

    # Copia lo stesso valore nelle tre colonne successive alla terza
    for i in range(3, 6):  # Colonne 4, 5 e 6 (indice 3, 4, 5)
        if i < len(df_csv.columns):  # Controlla che la colonna esista
            df_csv.loc[mask, df_csv.columns[i]] = df_csv.loc[mask, df_csv.columns[2]]

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def process_csv_events(df_csv, conn, db_table, db_column_eng, db_column_ita , search_value):
    """
    Funzione che aggiorna le colonne del CSV basandosi sulla tabella WARNINGS nel database.

    - Sostituisce 'Default', 'EN', 'FR' nel CSV con la colonna 'INGLESE' del database.
    - Sostituisce 'IT' nel CSV con la colonna 'ITALIANO' del database.
    - Filtra solo le righe che iniziano con `search_value` nella prima colonna.

    :param df_csv: DataFrame con i dati del CSV
    :param conn: Connessione al database SQLite
    :param db_table: Nome della tabella nel database
    :param search_value: Valore da cercare nella prima colonna del CSV
    """
    
    check_table_exists(conn, db_table)

    """if not check_table_exists(conn, db_table):
        print(f"❌ ERRORE: La tabella '{db_table}' non esiste nel database.")
        return"""
    
    # Query per prendere i dati dalla tabella specificata
    query = f"SELECT {db_column_eng, db_column_ita} FROM '{db_table}'"
    df_db = pd.read_sql(query, conn)

    # Identifica le righe che contengono il valore di ricerca nella prima colonna
    mask = df_csv.iloc[:, 0] == search_value

    # Controlla se ci sono abbastanza valori nel database
    num_replacements = mask.sum()
    if num_replacements == 0:
        print(f"⚠️ ATTENZIONE: Nessuna riga trovata con '{search_value}' nel CSV.")
        return
    if num_replacements != len(df_db) :
        print(f"Attenzione: il numero di righe tra database e file .csv {search_value} / {db_table} è diverso.")
        return
    
    print(f"Colonne disponibili nel database {db_table}: {df_db.columns.tolist()}")


    # -----> Sostituisce le colonne nel CSV <-----
    df_csv.loc[mask, "Default"] = df_db["ENG"].values[:num_replacements]  # INGLESE → Default
    df_csv.loc[mask, "EN"] = df_db["ENG"].values[:num_replacements]       # INGLESE → EN
    df_csv.loc[mask, "FR"] = df_db["ENG"].values[:num_replacements]       # INGLESE → FR
    df_csv.loc[mask, "IT"] = df_db["ITA"].values[:num_replacements]      # ITALIANO → IT

    print(f"✅ SUCCESSO: Aggiornate {num_replacements} righe con dati da '{db_table}'.")