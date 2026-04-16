import pandas as pd
import os

COLUMN_RENAME = {
    "DATE DE CLASSEMENT": "date_classement",
    "TYPOLOGIE ÉTABLISSEMENT": "type_hebergement",
    "CLASSEMENT": "classement",
    "CATÉGORIE": "categorie",
    "MENTION (villages de vacances)": "mention",
    "NOM COMMERCIAL": "nom",
    "ADRESSE": "adresse",
    "CODE POSTAL": "code_postal",
    "COMMUNE": "commune",
    "SITE INTERNET": "site_internet",
    "TYPE DE SÉJOUR": "type_sejour",
    "CAPACITÉ D'ACCUEIL (PERSONNES)": "capacite",
    "NOMBRE DE CHAMBRES": "nb_chambres",
    "NOMBRE D'EMPLACEMENTS": "nb_emplacements",
    "NOMBRE D'UNITES D'HABITATION (résidences de tourisme)": "nb_unites",
    "NOMBRE DE LOGEMENTS (villages de vacances)": "nb_logements",
    "classement prorogé": "classement_proroge"
}

def clean_data():
    print("Nettoyage...")
    df = pd.read_csv("data/raw/hebergements_raw.csv", sep=";", encoding="utf-8")

    # Renommer colonnes
    df = df.rename(columns=COLUMN_RENAME)

    # Supprimer doublons
    df = df.drop_duplicates()

    # Supprimer lignes sans nom ou commune
    df = df.dropna(subset=["nom", "commune"])

    # Remplacer "-" par None
    df = df.replace("-", None)

    # Conversion types
    df["capacite"] = pd.to_numeric(df["capacite"], errors="coerce")
    df["nb_chambres"] = pd.to_numeric(df["nb_chambres"], errors="coerce")
    df["nb_emplacements"] = pd.to_numeric(df["nb_emplacements"], errors="coerce")
    df["code_postal"] = df["code_postal"].astype(str).str.zfill(5)

    # Extraire département depuis code postal
    df["departement"] = df["code_postal"].str[:2]

    # Normaliser classement (garder juste le chiffre)
    df["nb_etoiles"] = df["classement"].str.extract(r"(\d)").astype(float)

    # Remplacer tous les NaN par None (compatible PostgreSQL)
    df = df.where(pd.notna(df), None)

    os.makedirs("data/clean", exist_ok=True)
    df.to_csv("data/clean/hebergements_clean.csv", index=False)
    print(f" Clean OK — {len(df)} lignes")
    return df