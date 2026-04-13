from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://mongo:27017/")
db = client["hebergement"]

def insert_raw():
    df = pd.read_csv("data/raw/hebergements_raw.csv")
    db.raw.delete_many({})
    db.raw.insert_many(df.to_dict("records"))
    print("Mongo RAW OK")

def insert_clean():
    df = pd.read_csv("data/clean/hebergements_clean.csv")
    db.clean.delete_many({})
    db.clean.insert_many(df.to_dict("records"))
    print("Mongo CLEAN OK")
