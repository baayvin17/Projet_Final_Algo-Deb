import pandas as pd
import os

def fetch_data():
    print("Chargement données depuis CSV public...")

    csv_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"

    return csv_url

def save_raw(csv_url):
    # créer dossier si existe pas
    os.makedirs("data/raw", exist_ok=True)

    df = pd.read_csv(csv_url)

    df.to_csv("data/raw/hebergements_raw.csv", index=False)

    print("Données RAW sauvegardées")
