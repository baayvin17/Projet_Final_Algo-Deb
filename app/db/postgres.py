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
            print(" Postgres connecté")
            return conn
        except Exception as e:
            print(f"Retry Postgres... {i}")
            time.sleep(3)
    raise Exception("Postgres not ready")

def insert_dw():
    conn = connect()
    cursor = conn.cursor()
    df = pd.read_csv("data/clean/hebergements_clean.csv")

    # Table principale
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hebergements (
        id SERIAL PRIMARY KEY,
        nom TEXT,
        type_hebergement TEXT,
        classement TEXT,
        nb_etoiles FLOAT,
        adresse TEXT,
        code_postal TEXT,
        commune TEXT,
        departement TEXT,
        site_internet TEXT,
        capacite FLOAT,
        nb_chambres FLOAT,
        nb_emplacements FLOAT,
        date_classement TEXT,
        classement_proroge TEXT
    );
    """)

    # Table dimension type
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_type_hebergement (
        id SERIAL PRIMARY KEY,
        type_hebergement TEXT UNIQUE
    );
    """)

    # Table dimension departement
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_departement (
        id SERIAL PRIMARY KEY,
        departement TEXT UNIQUE
    );
    """)

    conn.commit()
    cursor.execute("TRUNCATE TABLE hebergements CASCADE;")
    cursor.execute("TRUNCATE TABLE dim_type_hebergement CASCADE;")
    cursor.execute("TRUNCATE TABLE dim_departement CASCADE;")
    conn.commit()

    # Remplir dimensions
    for t in df["type_hebergement"].dropna().unique():
        cursor.execute("INSERT INTO dim_type_hebergement (type_hebergement) VALUES (%s) ON CONFLICT DO NOTHING",(str(t),))

    for d in df["departement"].dropna().unique():
        cursor.execute("INSERT INTO dim_departement (departement) VALUES (%s) ON CONFLICT DO NOTHING", (str(d),))

    # Remplir faits
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO hebergements 
        (nom, type_hebergement, classement, nb_etoiles, adresse, code_postal,
         commune, departement, site_internet, capacite, nb_chambres,
         nb_emplacements, date_classement, classement_proroge)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row.get("nom"), row.get("type_hebergement"), row.get("classement"),
            row.get("nb_etoiles"), row.get("adresse"), row.get("code_postal"),
            row.get("commune"), row.get("departement"), row.get("site_internet"),
            row.get("capacite"), row.get("nb_chambres"), row.get("nb_emplacements"),
            row.get("date_classement"), row.get("classement_proroge")
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(" DW OK")