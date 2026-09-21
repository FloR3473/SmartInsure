import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_loader import load_customers


# ---------------------------------------------------------
# Chargement du chemin de sortie
# ---------------------------------------------------------
OUTPUT_DIR = Path("graphiques")

# Création du dossier de sortie
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Style des graphiques
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# Chargement de la base Sqlite
# ---------------------------------------------------------
df = load_customers()

# ---------------------------------------------------------
# Séparation des colonnes
# ---------------------------------------------------------
numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

categorical_columns = df.select_dtypes(exclude=np.number).columns.tolist()

columns_to_exclude = ["customer", "response", "effective_to_date"]

categorical_columns = [column for column in categorical_columns
    if column not in columns_to_exclude]

# ============================================================
# Création des histogrammes
# ============================================================

for column in numeric_columns:

    plt.figure(figsize=(8, 5))

    sns.histplot(data=df, x=column, kde=True, bins=30)
    # Calcul de la moyenne
    mean = df[column].mean()

    # Ligne de la moyenne
    plt.axvline(mean, color="red", linestyle="--", label=f"Moyenne : {mean:.2f}")
    plt.legend()

    plt.title(f"Distribution - {column}")
    plt.xlabel(column)
    plt.ylabel("Nombre de clients")

    plt.tight_layout()

    filename = (OUTPUT_DIR / f"distribution_{column}.png")

    plt.savefig(filename, dpi=300, bbox_inches="tight")

    plt.close()

# ============================================================
# Création des graphiques catégoriels
# ============================================================

for column in categorical_columns:
    if df[column].nunique(dropna=True) > 20:
        continue

    plt.figure(figsize=(10, 6))

    order = (df[column].value_counts().index)

    sns.countplot(data=df, x=column, order=order)

    plt.title(f"Distribution - {column}")

    plt.xticks(rotation=45)

    plt.tight_layout()

    filename = (OUTPUT_DIR / f"countplot_{column}.png" )

    plt.savefig(filename, dpi=300, bbox_inches="tight")

    plt.close()