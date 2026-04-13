import psycopg2
import time
import pandas as pd

def connect():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host="postgres_dw",
                database="dw",
                user="postgres",
                password="postgres"
            )
            print("Postgres OK")
            return conn
        except Exception as e:
            print("Retry Postgres...", i)
            time.sleep(3)

    raise Exception("Postgres not ready")

def insert_dw():
    print("Connexion Postgres...")

    conn = connect()
    cursor = conn.cursor()

    df = pd.read_csv("data/clean/hebergements_clean.csv")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tips (
        id SERIAL PRIMARY KEY,
        total_bill FLOAT,
        tip FLOAT,
        sex TEXT,
        smoker TEXT,
        day TEXT,
        time TEXT,
        size INT
    );
    """)

    conn.commit()

    cursor.execute("TRUNCATE TABLE tips;")
    conn.commit()

    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO tips (total_bill, tip, sex, smoker, day, time, size)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["total_bill"],
            row["tip"],
            row["sex"],
            row["smoker"],
            row["day"],
            row["time"],
            row["size"]
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print("DW OK")