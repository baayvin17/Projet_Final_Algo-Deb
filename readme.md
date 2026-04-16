# 📊 PROJET FINAL – DATA PIPELINE (Scraping → ETL → API)

---

# 1. README – LANCEMENT DU PROJET

## 🚀 Description

Ce projet est un pipeline de données complet :

* Scraping de données CSV
* Nettoyage et transformation
* Stockage Data Lake (CSV / JSON)
* Stockage MongoDB (RAW + CLEAN)
* Data Warehouse PostgreSQL
* API REST avec FastAPI

---

## 🧱 Architecture

Flux de données :

```
CSV (source)
   ↓
Scraping
   ↓
Cleaning
   ↓
MongoDB (RAW + CLEAN)
   ↓
Data Lake (CSV/JSON)
   ↓
PostgreSQL (DW)
   ↓
API REST (FastAPI)
```

---

# 2. TECHNOLOGIES

* Python 3.11
* Pandas
* MongoDB
* PostgreSQL
* FastAPI
* Docker / Docker Compose

---

# 3. INSTALLATION & LANCEMENT

## 📦 1. Cloner le projet

```bash
git clone <repo>
cd Projet_Final
```

---

## 🐳 2. Lancer avec Docker dans 1er Terminal

```bash
docker compose down -v
docker compose up --build
```

---

## 🔥 3. Vérifier les containers dans un 2eme Terminal 

```bash
docker ps
```

Attendu :

* api
* postgres_dw
* mongo_db
* app_data

---

Lancer la page web : 

* Fichier html : LiveServer

---

# 4. PIPELINE AUTOMATIQUE

Le pipeline s’exécute automatiquement au démarrage :

### Étapes :

1. Lecture CSV brut
2. Nettoyage des données
3. Insertion MongoDB RAW
4. Insertion MongoDB CLEAN
5. Export Data Lake
6. Chargement PostgreSQL (DW)

---

# 5. BASE DE DONNÉES (POSTGRESQL)

Table principale :

```sql
tips (
    id SERIAL,
    total_bill FLOAT,
    tip FLOAT,
    sex TEXT,
    smoker TEXT,
    day TEXT,
    time TEXT,
    size INT
)
```

---

# Vérifier PostgreSQL dans le 2 eme Terminal
docker exec -it postgres_dw psql -U postgres

\c dw
SELECT * FROM tips LIMIT 5;

# 6. Lancer l’API dans un 3eme Terminal 
uvicorn app.api.main:app --reload

Endpoints :

http://localhost:8000/
http://localhost:8000/docs#/
http://localhost:8000/tips
http://localhost:8000/stats

# Lancer le Dashboard dans un 4eme Terminal
streamlit run streamlit_app.py
📊 Dashboard

Le dashboard Streamlit permet :

visualisation des KPI
analyse des tips
filtres interactifs
🖼️ Scraping

Une image est téléchargée automatiquement :

docker compose run app_data
docker cp NOM:/app/data/images ./images
## Endpoints

### GET /

Retour statut API

---

### GET /tips

Retour des données DW

```json
[
  {
    "id": 1,
    "total_bill": 16.99,
    "tip": 1.01
  }
]
```

---

### GET /stats

Retour statistiques globales :

* moyenne facture
* moyenne tips

---

# 7. DATA LAKE

Stockage :

* `data/raw/`
* `data/clean/`

Format :

* CSV

---

# 8. MONGODB

Collections :

* raw_data
* clean_data

Objectif :

* historisation des données
* traçabilité ETL

---

# 9. QUALITÉ DES DONNÉES

Traitements :

* suppression doublons
* suppression valeurs nulles
* normalisation colonnes

---

# 10. DATA ENGINEERING (ARCHITECTURE)

Respect des principes :

* séparation des couches
* modularité
* pipeline automatisé
* conteneurisation

---

# 11. LIMITES

* pas de streaming temps réel
* pas de dashboard BI
* tests unitaires limités

---

# 12. AMÉLIORATIONS POSSIBLES

* ajout Power BI / Metabase
* tests Pytest complets
* orchestration Airflow
* CI/CD GitHub Actions

---

# 13. CONCLUSION

Ce projet démontre :

✔ ingestion de données
✔ transformation ETL
✔ stockage multi-systèmes
✔ exposition API REST

