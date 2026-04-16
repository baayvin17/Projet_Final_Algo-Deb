from fastapi import FastAPI, Query
import psycopg2
import pandas as pd

app = FastAPI(
    title="API Hébergements Touristiques ",
    description="API REST pour explorer les hébergements classés en France (source : Atout France / data.gouv.fr)",
    version="1.0.0"
)

# ---------------------------
# CONNEXION POSTGRESQL
# ---------------------------
def get_conn():
    return psycopg2.connect(
        host="postgres_dw",
        database="dw",
        user="postgres",
        password="postgres"
    )


# ---------------------------
# ROUTE 1 : HOME
# ---------------------------
@app.get("/")
def home():
    return {"message": "API Hébergements Touristiques OK "}


# ---------------------------
# ROUTE 2 : GET HEBERGEMENTS
# Filtres : type, departement, nb_etoiles
# Pagination : limit + offset
# ---------------------------
@app.get("/hebergements")
def get_hebergements(
    limit: int = Query(10, ge=1, le=100, description="Nombre de résultats"),
    offset: int = Query(0, ge=0, description="Décalage pour la pagination"),
    type_hebergement: str = Query(None, description="Ex: HÔTEL DE TOURISME, CAMPING"),
    departement: str = Query(None, description="Ex: 75, 13, 69"),
    nb_etoiles: float = Query(None, description="Ex: 1, 2, 3, 4, 5"),
    commune: str = Query(None, description="Ex: PARIS, LYON")
):
    conn = get_conn()

    query = "SELECT * FROM hebergements WHERE 1=1"
    params = []

    if type_hebergement:
        query += " AND type_hebergement ILIKE %s"
        params.append(f"%{type_hebergement}%")

    if departement:
        query += " AND departement = %s"
        params.append(departement)

    if nb_etoiles is not None:
        query += " AND nb_etoiles = %s"
        params.append(nb_etoiles)

    if commune:
        query += " AND commune ILIKE %s"
        params.append(f"%{commune}%")

    query += " ORDER BY id LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


# ---------------------------
# ROUTE 3 : STATS GLOBALES
# ---------------------------
@app.get("/stats")
def get_stats():
    conn = get_conn()
    df = pd.read_sql("""
        SELECT
            COUNT(*)                        AS total_hebergements,
            ROUND(AVG(nb_etoiles)::numeric, 2)  AS moyenne_etoiles,
            ROUND(AVG(capacite)::numeric, 2)    AS moyenne_capacite,
            SUM(capacite)                   AS capacite_totale,
            SUM(nb_chambres)                AS total_chambres,
            SUM(nb_emplacements)            AS total_emplacements
        FROM hebergements
    """, conn)
    conn.close()
    return df.to_dict(orient="records")[0]


# ---------------------------
# ROUTE 4 : STATS PAR TYPE
# ---------------------------
@app.get("/stats/type")
def stats_par_type():
    conn = get_conn()
    df = pd.read_sql("""
        SELECT
            type_hebergement,
            COUNT(*)                            AS nb_hebergements,
            ROUND(AVG(nb_etoiles)::numeric, 2)  AS moyenne_etoiles,
            SUM(capacite)                       AS capacite_totale
        FROM hebergements
        GROUP BY type_hebergement
        ORDER BY nb_hebergements DESC
    """, conn)
    conn.close()
    return df.to_dict(orient="records")


# ---------------------------
# ROUTE 5 : STATS PAR DEPARTEMENT
# ---------------------------
@app.get("/stats/departement")
def stats_par_departement(limit: int = Query(20, ge=1, le=100)):
    conn = get_conn()
    df = pd.read_sql(f"""
        SELECT
            departement,
            COUNT(*)        AS nb_hebergements,
            SUM(capacite)   AS capacite_totale,
            ROUND(AVG(nb_etoiles)::numeric, 2) AS moyenne_etoiles
        FROM hebergements
        GROUP BY departement
        ORDER BY nb_hebergements DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df.to_dict(orient="records")


# ---------------------------
# ROUTE 6 : STATS PAR CLASSEMENT
# ---------------------------
@app.get("/stats/classement")
def stats_par_classement():
    conn = get_conn()
    df = pd.read_sql("""
        SELECT
            classement,
            COUNT(*) AS nb_hebergements,
            SUM(capacite) AS capacite_totale
        FROM hebergements
        WHERE classement IS NOT NULL
        GROUP BY classement
        ORDER BY nb_hebergements DESC
    """, conn)
    conn.close()
    return df.to_dict(orient="records")


# ---------------------------
# ROUTE 7 : TOP HEBERGEMENTS PAR CAPACITE
# ---------------------------
@app.get("/top")
def top_hebergements(limit: int = Query(10, ge=1, le=50)):
    conn = get_conn()
    df = pd.read_sql(f"""
        SELECT
            nom,
            type_hebergement,
            commune,
            departement,
            classement,
            nb_etoiles,
            capacite,
            nb_chambres
        FROM hebergements
        WHERE capacite IS NOT NULL
        ORDER BY capacite DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df.to_dict(orient="records")


# ---------------------------
# ROUTE 8 : RECHERCHE PAR NOM
# ---------------------------
@app.get("/recherche")
def recherche(
    q: str = Query(..., description="Nom ou mot-clé à rechercher"),
    limit: int = Query(10, ge=1, le=50)
):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM hebergements
        WHERE nom ILIKE %s
        ORDER BY nom
        LIMIT %s
    """, conn, params=(f"%{q}%", limit))
    conn.close()
    return df.to_dict(orient="records")


# ---------------------------
# ROUTE 9 : DETAIL PAR ID
# ---------------------------
@app.get("/hebergements/{id}")
def get_hebergement_by_id(id: int):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM hebergements WHERE id = %s
    """, conn, params=(id,))
    conn.close()
    if df.empty:
        return {"error": f"Hébergement {id} non trouvé"}
    return df.to_dict(orient="records")[0]