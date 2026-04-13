import pandas as pd
import os

def clean_data():
    print("Cleaning...")

    df = pd.read_csv("data/raw/hebergements_raw.csv")

    df = df.drop_duplicates()
    df = df.dropna()

    os.makedirs("data/clean", exist_ok=True)

    path = "data/clean/hebergements_clean.csv"
    df.to_csv(path, index=False)

    print("Clean OK")
    return df