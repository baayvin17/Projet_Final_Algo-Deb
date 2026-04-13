import pandas as pd
import os

def save_lake():
    # créer dossier si il n'existe pas
    os.makedirs("data/lake", exist_ok=True)

    df = pd.read_csv("data/clean/hebergements_clean.csv")

    df.to_json("data/lake/hebergements.json", orient="records")

    print("Data Lake JSON OK")
