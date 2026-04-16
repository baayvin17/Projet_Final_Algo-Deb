from fastapi import FastAPI, Query
from fastapi.responses import Response
from sqlalchemy import create_engine, text
import pandas as pd
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Hébergements Touristiques 🏨",
    description="API REST - Hébergements classés en France (Atout France / data.gouv.fr)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@postgres_dw:5432/dw"


# ---------------------------
# HELPERS
# ---------------------------
def get_engine():
    return create_engine(DATABASE_URL)


def query_df(sql, params=None):
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn, params=params or {})
    return df


def to_json(df):
    """Retourne une liste — pandas gère NaN → null nativement"""
    return Response(
        content=df.to_json(orient="records", force_ascii=False),
        media_type="application/json"
    )


def to_json_single(df):
    """Retourne un seul objet JSON"""
    records = json.loads(df.to_json(orient="records", force_ascii=False))
    return Response(
        content=json.dumps(records[0], ensure_ascii=False),
        media_type="application/json"
    )


# ---------------------------
# ROUTE 1 : HOME
# ---------------------------
@app.get("/")
def home():
    return {"message": "API Hébergements Touristiques OK 🏨"}


# ---------------------------
# ROUTE 2 : GET HEBERGEMENTS
# Filtres : type, departement, nb_etoiles, commune
# Pagination : limit + offset
# ---------------------------
@app.get("/hebergements")
def get_hebergements(
    limit: int = Query(10, ge=1, le=25000, description="Nombre de résultats"),
    offset: int = Query(0, ge=0, description="Décalage pour la pagination"),
    type_hebergement: str = Query(None, description="Ex: HÔTEL DE TOURISME, CAMPING"),
    departement: str = Query(None, description="Ex: 75, 13, 69"),
    nb_etoiles: float = Query(None, description="Ex: 1, 2, 3, 4, 5"),
    commune: str = Query(None, description="Ex: PARIS, LYON")
):
    sql = "SELECT * FROM hebergements WHERE 1=1"
    params = {}

    if type_hebergement:
        sql += " AND type_hebergement ILIKE :type_hebergement"
        params["type_hebergement"] = f"%{type_hebergement}%"

    if departement:
        sql += " AND departement = :departement"
        params["departement"] = departement

    if nb_etoiles is not None:
        sql += " AND nb_etoiles = :nb_etoiles"
        params["nb_etoiles"] = nb_etoiles

    if commune:
        sql += " AND commune ILIKE :commune"
        params["commune"] = f"%{commune}%"

    sql += " ORDER BY id LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    df = query_df(sql, params)
    return to_json(df)


# ---------------------------
# ROUTE 3 : STATS GLOBALES
# ---------------------------
@app.get("/stats")
def get_stats():
    df = query_df("""
        SELECT
            COUNT(*)                            AS total_hebergements,
            ROUND(AVG(nb_etoiles)::numeric, 2)  AS moyenne_etoiles,
            ROUND(AVG(capacite)::numeric, 2)    AS moyenne_capacite,
            SUM(capacite)                       AS capacite_totale,
            SUM(nb_chambres)                    AS total_chambres,
            SUM(nb_emplacements)                AS total_emplacements
        FROM hebergements
    """)
    return to_json_single(df)


# ---------------------------
# ROUTE 4 : STATS PAR TYPE
# ---------------------------
@app.get("/stats/type")
def stats_par_type():
    df = query_df("""
        SELECT
            type_hebergement,
            COUNT(*)                            AS nb_hebergements,
            ROUND(AVG(nb_etoiles)::numeric, 2)  AS moyenne_etoiles,
            SUM(capacite)                       AS capacite_totale
        FROM hebergements
        GROUP BY type_hebergement
        ORDER BY nb_hebergements DESC
    """)
    return to_json(df)


# ---------------------------
# ROUTE 5 : STATS PAR DEPARTEMENT
# ---------------------------
@app.get("/stats/departement")
def stats_par_departement(limit: int = Query(20, ge=1, le=100)):
    df = query_df("""
        SELECT
            departement,
            COUNT(*)        AS nb_hebergements,
            SUM(capacite)   AS capacite_totale,
            ROUND(AVG(nb_etoiles)::numeric, 2) AS moyenne_etoiles
        FROM hebergements
        GROUP BY departement
        ORDER BY nb_hebergements DESC
        LIMIT :limit
    """, {"limit": limit})
    return to_json(df)


# ---------------------------
# ROUTE 6 : STATS PAR CLASSEMENT
# ---------------------------
@app.get("/stats/classement")
def stats_par_classement():
    df = query_df("""
        SELECT
            classement,
            COUNT(*) AS nb_hebergements,
            SUM(capacite) AS capacite_totale
        FROM hebergements
        WHERE classement IS NOT NULL
        GROUP BY classement
        ORDER BY nb_hebergements DESC
    """)
    return to_json(df)


# ---------------------------
# ROUTE 7 : TOP HEBERGEMENTS PAR CAPACITE
# ---------------------------
@app.get("/top")
def top_hebergements(limit: int = Query(10, ge=1, le=50)):
    df = query_df("""
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
        LIMIT :limit
    """, {"limit": limit})
    return to_json(df)


# ---------------------------
# ROUTE 8 : RECHERCHE PAR NOM
# ---------------------------
@app.get("/recherche")
def recherche(
    q: str = Query(..., description="Nom ou mot-clé à rechercher"),
    limit: int = Query(10, ge=1, le=50)
):
    df = query_df("""
        SELECT * FROM hebergements
        WHERE nom ILIKE :q
        ORDER BY nom
        LIMIT :limit
    """, {"q": f"%{q}%", "limit": limit})
    return to_json(df)


# ---------------------------
# ROUTE 9 : DETAIL PAR ID
# ---------------------------
@app.get("/hebergements/{id}")
def get_by_id(id: int):
    df = query_df("""
        SELECT * FROM hebergements WHERE id = :id
    """, {"id": id})
    if df.empty:
        return Response(
            content=json.dumps({"error": f"Hébergement {id} non trouvé"}),
            media_type="application/json"
        )
    return to_json_single(df)