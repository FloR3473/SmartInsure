import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_loader import load_customers

# ---------------------------------------------------------
# Chargement de la base Sqlite
# ---------------------------------------------------------
df = load_customers()

# ---------------------------------------------------------
# Création de la matrice de corrélation
# ---------------------------------------------------------
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