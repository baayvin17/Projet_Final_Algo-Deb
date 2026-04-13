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

## 🐳 2. Lancer avec Docker

```bash
docker compose down -v
docker compose up --build
```

---

## 🔥 3. Vérifier les containers

```bash
docker ps
```

Attendu :

* api
* postgres_dw
* mongo_db
* app_data

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

# 6. API REST

## 📌 Lancement API

```
http://localhost:8000/docs
```

---

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

---

# 🧠 RÉSUMÉ PROFESSEUR

Le projet montre une chaîne complète de data engineering :

* source → traitement → stockage → exposition

---

# 🚀 FIN DU PROJET
