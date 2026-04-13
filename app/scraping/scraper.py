import pandas as pd
import os
import requests

# ---------------------------
# FETCH DATA
# ---------------------------
def fetch_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
    df = pd.read_csv(url)
    return df

# ---------------------------
# SAVE RAW
# ---------------------------
def save_raw(df):
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/tips_raw.csv", index=False)
    print("Données RAW sauvegardées")

# ---------------------------
# DOWNLOAD IMAGE
# ---------------------------
def download_image():
    url = "http://placekitten.com/300/300"

    os.makedirs("data/images", exist_ok=True)
    path = "data/images/sample.jpg"

    try:
        print("Téléchargement image...")
        r = requests.get(url, timeout=10)

        with open(path, "wb") as f:
            f.write(r.content)

        print("Image téléchargée OK")

    except Exception as e:
        print("Erreur téléchargement image :", e)
