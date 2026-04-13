from fastapi import FastAPI
from pymongo import MongoClient
import statistics

app = FastAPI()

# Connexion Mongo (Docker)
client = MongoClient("mongodb://mongo_db:27017/")
db = client["hebergement"]
collection = db["clean"]

# ---------------------------
# ROUTE 1 : HOME
# ---------------------------
@app.get("/")
def home():
    return {"message": "API Tips OK 🔥"}

# ---------------------------
# ROUTE 2 : GET TIPS
# ---------------------------
@app.get("/tips")
def get_tips(limit: int = 10):
    data = list(collection.find({}, {"_id": 0}).limit(limit))
    return data

# ---------------------------
# ROUTE 3 : STATS
# ---------------------------
@app.get("/stats")
def get_stats():
    data = list(collection.find({}, {"_id": 0}))

    total_bills = [d["total_bill"] for d in data]
    tips = [d["tip"] for d in data]

    return {
        "total_transactions": len(data),
        "avg_total_bill": round(statistics.mean(total_bills), 2),
        "avg_tip": round(statistics.mean(tips), 2),
        "max_tip": max(tips),
        "min_tip": min(tips)
    }

# ---------------------------
# ROUTE 4 : FILTER PAR JOUR
# ---------------------------
@app.get("/tips/day/{day}")
def tips_by_day(day: str):
    data = list(collection.find(
        {"day": day.capitalize()},
        {"_id": 0}
    ))
    return data

# ---------------------------
# ROUTE 5 : TOP TIPS
# ---------------------------
@app.get("/top_tips")
def top_tips():
    data = list(collection.find({}, {"_id": 0}))
    sorted_data = sorted(data, key=lambda x: x["tip"], reverse=True)
    return sorted_data[:5]
