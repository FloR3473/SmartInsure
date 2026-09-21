import pandas as pd
from pathlib import Path
from datetime import datetime
import sqlite3 

# ---------------------------------------------------------
# 1) Configuration des chemins d'accès
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "AutoInsurance.csv"

DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "smartinsure.db"
DB_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# 1) EXTRACT - EXTRACTION DES DONNEES DANS LA VARIABLE df
# ---------------------------------------------------------
def extract_data():
    df = pd.read_csv(DATA_PATH, sep=",", encoding="utf-8-sig")

    print("DataFrame créé")
    print("Dimensions :", df.shape)

    return df

# ---------------------------------------------------------
# 2) TRANSFORM - NETTOYAGE DES TYPES DE DONNEES
# ---------------------------------------------------------
def tranform_data(df):
    # Normalisation du nom des colonnes
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        )

    # Vérification des valeurs manquantes
    print(f"Il y a", sum(df.isna().sum()), "valeur(s) manquante(s)")

    # Vérification des types de valeur
    print(df.info())

    # Mise au format date
    df["effective_to_date"] = pd.to_datetime(df["effective_to_date"], format="mixed", errors="coerce")

    # Vérification des doublons
    duplicates_before = df.duplicated().sum()

    if duplicates_before > 0:
        df = df.drop_duplicates()
        print(f"\nDoublons supprimés : {duplicates_before}")
    else:
        print("\nAucun doublon détecté.")

    # Vérification des valeurs aberrantes
    for column in df.columns:
        print(f"\n--- {column} ---")

        if df[column].dtype == "str":
            print("Valeurs uniques :", df[column].unique())
            print("Nombre de valeurs uniques :", df[column].nunique())
        else:
            print(df[column].describe())

    # Vérification et remplacement des valeurs négatives.
    numeric_columns = [
        "customer_lifetime_value",
        "income",
        "monthly_premium_auto",
        "months_since_last_claim",
        "months_since_policy_inception",
        "number_of_open_complaints",
        "number_of_policies",
        "total_claim_amount",
    ]

    for column in numeric_columns:
        if column in df.columns:
            negative_count = (df[column] < 0).sum()

            if negative_count > 0:
                print("\nValeur(s) négative(s) trouvée(s) :")
                print(f"    -> {column} : {negative_count} ")

                df.loc[df[column] < 0, column] *= -1


# ---------------------------------------------------------
# 3) LOAD - BASE DE DONNEES SQLITE
# ---------------------------------------------------------
def load_to_sqlite(df):
    print("\nChargement de la base de données SQLITE")

    connection = sqlite3.connect(DB_PATH)

    try:
        df.to_sql("customers", connection, if_exists="replace", index=False)

        print(f"Base de données créée : {DB_PATH}")
        print("Table créée : customers")

        # Vérification
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        count = cursor.fetchone()[0]

        print(f"Nombre de lignes dans SQL : {count}")

    finally:
        connection.close()

    print("\nChargement SQL terminé.")




# ---------------------------------------------------------
# 4) FONCTION PRINCIPALE
# ---------------------------------------------------------
def run_etl():
    df = extract_data()
    tranform_data(df)
    load_to_sqlite(df)


run_etl()