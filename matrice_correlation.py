# ============================================================
# ANALYSE EXPLORATOIRE - TABLE CUSTOMERS
# ============================================================

import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. CONFIGURATION
# ============================================================
BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "smartinsure.db"
OUTPUT_DIR = Path("eda_results")

# Création du dossier de sortie
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Charger la base Sqlite
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM customers",conn)
conn.close()

# Supprimer les colonnes qu'on ne veut pas analyser
df = df.drop(
    columns=["customer","effective_to_date", "response"],
    errors="ignore")

# Transformer les colonnes texte en nombres
df_encoded = pd.get_dummies(df, drop_first=True)

# Calculer les corrélations
correlation_matrix = df_encoded.corr()

# Afficher la matrice sous format graphique
plt.figure(figsize=(18, 14))
sns.heatmap(correlation_matrix, cmap="coolwarm", center=0, annot=False)
plt.title("Matrice de corrélation")
plt.tight_layout()
plt.show()

print("Matrice de corrélation réalisée")