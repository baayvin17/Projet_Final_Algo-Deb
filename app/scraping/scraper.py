import pandas as pd
import os
import requests

CSV_URL = "https://data.classement.atout-france.fr/static/exportHebergementsClasses/hebergements_classes.csv"

# ---------------------------
# FETCH DATA
# ---------------------------
def fetch_data():
    try:
        print("Téléchargement données Atout France...")
        df = pd.read_csv(CSV_URL, sep=";", encoding="utf-8")
        print(f" {len(df)} hébergements récupérés")
        return df
    except Exception as e:
        print(f" Erreur fetch : {e}")
        raise
# ---------------------------
# SAVE RAW
# ---------------------------
def save_raw(df):
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/hebergements_raw.csv", sep=";", index=False)
    print(" RAW sauvegardé")

# ---------------------------
# DOWNLOAD IMAGE
# ---------------------------
def download_image():
    url = "https://www.data.gouv.fr/img/logo-header.svg"
    os.makedirs("data/images", exist_ok=True)
    try:
        r = requests.get(url, timeout=10)
        with open("data/images/datagouv.svg", "wb") as f:
            f.write(r.content)
        print(" Image téléchargée")
    except Exception as e:
        print(f" Erreur image : {e}")