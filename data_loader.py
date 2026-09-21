from pathlib import Path
import sqlite3
import pandas as pd


# ---------------------------------------------------------
# Configuration des chemins
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "smartinsure.db"

# ---------------------------------------------------------
# Chargement de la base SQLite
# ---------------------------------------------------------

def load_customers():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df