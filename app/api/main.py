from fastapi import FastAPI
import psycopg2
import pandas as pd

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="postgres_dw",
        database="dw",
        user="postgres",
        password="postgres"
    )

@app.get("/")
def home():
    return {"status": "API OK"}

@app.get("/tips")
def get_tips(limit: int = 10):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM tips LIMIT {limit}", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/stats")
def stats():
    conn = get_conn()
    df = pd.read_sql("SELECT AVG(total_bill) as avg_bill, AVG(tip) as avg_tip FROM tips", conn)
    conn.close()
    return df.to_dict(orient="records")[0]