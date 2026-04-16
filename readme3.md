# 🏨 PROJET FINAL – DATA PIPELINE HÉBERGEMENTS TOURISTIQUES

---

## 🚀 Description

Pipeline de données complet basé sur les **hébergements touristiques classés en France**  
Source officielle : **Atout France / data.gouv.fr**

Étapes du pipeline :

- Scraping CSV depuis data.gouv.fr
- Nettoyage et transformation des données
- Stockage MongoDB (RAW + CLEAN)
- Export Data Lake (CSV / JSON)
- Data Warehouse PostgreSQL (schéma analytique)
- API REST avec FastAPI
- Dashboard BI avec Power BI

---

## 🧱 Architecture

```
CSV Atout France (data.gouv.fr)
   ↓
Scraping (scraper.py)
   ↓
Cleaning (cleaner.py)
   ↓
MongoDB RAW + CLEAN (mongo.py)
   ↓
Data Lake CSV/JSON (lake.py)
   ↓
PostgreSQL DW — schéma analytique (postgres.py)
   ↓
API REST FastAPI (main.py)
   ↓
Power BI (BI)
```

---

## 🗂️ Structure du projet

```
Projet_Final/
├── app/
│   ├── scraping/
│   │   └── scraper.py        # Téléchargement CSV Atout France
│   ├── cleaning/
│   │   └── cleaner.py        # Nettoyage et transformation
│   ├── db/
│   │   ├── mongo.py          # Insertion MongoDB RAW + CLEAN
│   │   ├── lake.py           # Export Data Lake JSON
│   │   └── postgres.py       # Chargement Data Warehouse
│   └── api/
│       └── main.py           # API REST FastAPI
├── data/
│   ├── raw/                  # CSV brut (séparateur ;)
│   ├── clean/                # CSV nettoyé
│   ├── lake/                 # JSON Data Lake
│   └── images/               # Image téléchargée
├── main.py                   # Point d'entrée pipeline
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🌍 Source des données

| Champ | Valeur |
|-------|--------|
| Jeu de données | Hébergements touristiques classés en France |
| Producteur | Atout France |
| Licence | Licence Ouverte / Open Licence |
| URL CSV | https://data.classement.atout-france.fr/static/exportHebergementsClasses/hebergements_classes.csv |
| Page data.gouv.fr | https://www.data.gouv.fr/datasets/hebergements-touristiques-classes-en-france |
| Volume | ~21 000 hébergements |

Types d'hébergements couverts : Hôtels de tourisme, Campings, Villages de vacances, Résidences de tourisme, Parcs résidentiels de loisirs, Auberges collectives.

---

## 🛠️ Technologies

| Outil | Usage |
|-------|-------|
| Python 3.11 | Langage principal |
| Pandas | Manipulation des données |
| MongoDB | Stockage RAW et CLEAN |
| PostgreSQL | Data Warehouse analytique |
| FastAPI | API REST |
| SQLAlchemy | Connecteur PostgreSQL |
| Docker / Docker Compose | Conteneurisation |
| Power BI | Dashboard BI |

---

## 📦 Installation & Lancement

### 1. Cloner le projet

```bash
git clone <repo>
cd Projet_Final
```

### 2. Lancer avec Docker (Terminal 1)

```bash
docker compose down -v
docker compose up --build
```

### 3. Vérifier les containers (Terminal 2)

```bash
docker ps
```

Containers attendus :

- `api` — FastAPI sur le port 8000
- `postgres_dw` — PostgreSQL sur le port 5432
- `mongo_db` — MongoDB sur le port 27017
- `app_data` — Pipeline ETL (s'exécute et se termine)

---

## ⚙️ Pipeline automatique

Le pipeline s'exécute automatiquement au démarrage du container `app_data` :

| Étape | Fichier | Description |
|-------|---------|-------------|
| 1 | scraper.py | Téléchargement CSV Atout France |
| 2 | scraper.py | Sauvegarde RAW (`data/raw/hebergements_raw.csv`) |
| 3 | scraper.py | Téléchargement image |
| 4 | cleaner.py | Nettoyage, normalisation, typage |
| 5 | mongo.py | Insertion MongoDB collection `raw` |
| 6 | mongo.py | Insertion MongoDB collection `clean` |
| 7 | lake.py | Export JSON (`data/lake/hebergements.json`) |
| 8 | postgres.py | Chargement PostgreSQL Data Warehouse |

---

## 🧹 Qualité des données (cleaner.py)

Traitements appliqués :

- Renommage des colonnes (suppression accents, majuscules, parenthèses)
- Suppression des doublons
- Suppression des lignes sans `nom` ni `commune`
- Remplacement des `"-"` par `null`
- Conversion des colonnes numériques (`capacite`, `nb_chambres`, `nb_emplacements`)
- Formatage `code_postal` en 5 chiffres (`str.zfill(5)`)
- Extraction du `departement` depuis le code postal (`str[:2]`)
- Extraction de `nb_etoiles` (valeur numérique) depuis la colonne `classement` textuelle
- Remplacement de tous les `NaN` par `None` (compatible PostgreSQL et MongoDB)

---

## 🗄️ Base de données PostgreSQL

### Table principale

```sql
hebergements (
    id                  SERIAL PRIMARY KEY,
    nom                 TEXT,
    type_hebergement    TEXT,
    classement          TEXT,
    nb_etoiles          FLOAT,
    adresse             TEXT,
    code_postal         TEXT,
    commune             TEXT,
    departement         TEXT,
    site_internet       TEXT,
    capacite            FLOAT,
    nb_chambres         FLOAT,
    nb_emplacements     FLOAT,
    date_classement     TEXT,
    classement_proroge  TEXT
)
```

### Tables de dimension

```sql
dim_type_hebergement (id SERIAL PRIMARY KEY, type_hebergement TEXT UNIQUE)
dim_departement      (id SERIAL PRIMARY KEY, departement TEXT UNIQUE)
```

### Vérifier PostgreSQL (Terminal 2)

```bash
docker exec -it postgres_dw psql -U postgres

\c dw
SELECT COUNT(*) FROM hebergements;
SELECT type_hebergement, COUNT(*) FROM hebergements GROUP BY type_hebergement;
SELECT * FROM hebergements LIMIT 5;
```

---

## 🍃 MongoDB

Collections :

- `raw` — données brutes telles que téléchargées
- `clean` — données nettoyées et transformées

Objectif : historisation des données et traçabilité ETL.

---

## 💧 Data Lake

| Dossier | Format | Contenu |
|---------|--------|---------|
| `data/raw/` | CSV (sep=`;`) | Données brutes Atout France |
| `data/clean/` | CSV | Données nettoyées |
| `data/lake/` | JSON | Export exploitable |

---

## 🔌 API REST

### Lancer l'API (Terminal 3)

```bash
uvicorn app.api.main:app --reload
```

### Documentation interactive

```
http://localhost:8000/docs
```

### Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/` | Statut API |
| GET | `/hebergements` | Liste avec filtres et pagination |
| GET | `/stats` | Statistiques globales |
| GET | `/stats/type` | Stats par type d'hébergement |
| GET | `/stats/departement` | Stats par département |
| GET | `/stats/classement` | Stats par classement |
| GET | `/top` | Top hébergements par capacité |
| GET | `/recherche?q=` | Recherche par nom |
| GET | `/hebergements/{id}` | Détail par ID |

### Paramètres de filtrage (`/hebergements`)

| Paramètre | Type | Exemple |
|-----------|------|---------|
| `limit` | int | `10` |
| `offset` | int | `0` |
| `type_hebergement` | string | `HÔTEL DE TOURISME` |
| `departement` | string | `75` |
| `nb_etoiles` | float | `4` |
| `commune` | string | `PARIS` |

### Exemple de réponse (`/hebergements`)

```json
[
  {
    "id": 1,
    "nom": "1924 HÔTEL",
    "type_hebergement": "HÔTEL DE TOURISME",
    "classement": "3 étoiles",
    "nb_etoiles": 3.0,
    "commune": "GRENOBLE",
    "departement": "38",
    "capacite": 62.0,
    "nb_chambres": 37.0
  }
]
```

---

## 📊 Power BI

### Connexion PostgreSQL

| Paramètre | Valeur |
|-----------|--------|
| Serveur | `localhost` |
| Port | `5432` |
| Base de données | `dw` |
| Utilisateur | `postgres` |
| Mot de passe | `postgres` |

### Visuels disponibles

- Répartition des hébergements par type
- Nombre d'hébergements par département
- Moyenne des étoiles par type d'hébergement
- Capacité totale d'accueil par département
- Top établissements par capacité

---

## 🏗️ Architecture & Principes

- Séparation stricte des couches (scraping / cleaning / storage / API)
- Un fichier par responsabilité (modularité)
- Pipeline automatisé au démarrage
- Conteneurisation complète Docker
- Gestion des erreurs sur le scraping et la connexion PostgreSQL (retry x10)

---

## ⚠️ Limites

- Pas de coordonnées GPS dans le dataset source (carte impossible)
- Pas de streaming temps réel
- Tests unitaires limités

---

## 🔮 Améliorations possibles

- Tests Pytest complets (unitaires + intégration)
- Orchestration Airflow
- CI/CD GitHub Actions
- Enrichissement avec un second dataset (fréquentation touristique)

---

## ✅ Conclusion

Ce projet démontre :

- ✔ Ingestion de données open data officielles (data.gouv.fr)
- ✔ Pipeline ETL complet et automatisé
- ✔ Stockage multi-systèmes (MongoDB + PostgreSQL + Data Lake)
- ✔ API REST avec filtres, pagination et 9 endpoints
- ✔ Exploitation BI via Power BI
- ✔ Conteneurisation Docker complète