from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/hebergements")
def get_all():
    df = pd.read_csv("data/clean/hebergements_clean.csv")
    return df.to_dict("records")

@app.get("/search")
def search(ville: str):
    df = pd.read_csv("data/clean/hebergements_clean.csv")
    result = df[df.apply(lambda x: ville.lower() in str(x).lower(), axis=1)]
    return result.to_dict("records")
