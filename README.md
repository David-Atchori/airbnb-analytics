# 🏠 Airbnb Analytics Platform

> **MBA ESG Paris — Promotion 2026**  
> Module : Management Opérationnel & DevOps Data  
> Soumission : `MBAESG_EVALUATION_MANAGEMENT_OPERATIONNEL_2026`

---

## 📋 Présentation du projet

Cette plateforme analytique permet d'exploiter les données Airbnb via une architecture **medallion** (Bronze → Silver → Gold), orchestrée par **dbt** et **DuckDB**, avec restitution via une application **Streamlit**.

### Cas d'usage couverts

| Analyse | Couche | Description |
|---|---|---|
| Logements | Gold | Type, prix, distribution géographique |
| Hôtes | Gold | Performance, taux superhost, ancienneté |
| Avis clients | Gold | Sentiment, évolution temporelle, recherche |
| Pleine lune × avis | Gold | Impact des nuits de pleine lune sur le sentiment |

---

## 🏗️ Architecture

```
Sources S3 (CSV/JSON)
        │
        ▼
  ┌─── BRONZE ─────────────────────────────────┐
  │  Ingestion brute via read_csv_auto (DuckDB) │
  │  bronze_hosts / bronze_reviews              │
  │  bronze_listings / bronze_full_moon_dates   │
  └─────────────────────────────────────────────┘
        │
        ▼
  ┌─── SILVER ─────────────────────────────────┐
  │  Nettoyage, typage, filtrage qualité        │
  │  silver_hosts / silver_reviews              │
  │  silver_listings / silver_full_moon_dates   │
  └─────────────────────────────────────────────┘
        │
        ▼
  ┌─── GOLD ───────────────────────────────────┐
  │  Data products & marts analytiques          │
  │  dim_hosts / dim_listings                   │
  │  fact_reviews                               │
  │  mart_full_moon_analysis                    │
  │  mart_host_performance                      │
  └─────────────────────────────────────────────┘
        │
        ▼
  ┌─── STREAMLIT ──────────────────────────────┐
  │  Dashboard interactif avec filtres dynamiques│
  │  4 onglets : Logements / Hôtes / Avis / Lune│
  └─────────────────────────────────────────────┘
```

### Stack technique

| Outil | Rôle |
|---|---|
| **DuckDB** | Moteur analytique in-process |
| **dbt-duckdb** | Transformations SQL et tests qualité |
| **Streamlit** | Dashboard interactif |
| **Plotly** | Visualisations |
| **GitHub** | Versioning collaboratif |

---

## ⚙️ Installation & Exécution

### Prérequis

- Python 3.10+
- Git

### 1. Cloner le dépôt

```bash
git clone https://github.com/<votre-org>/airbnb-analytics.git
cd airbnb-analytics
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
# ou
make install
```

### 3. Configurer le profil dbt

Le fichier `profiles.yml` est à la racine du projet. Il configure DuckDB avec le fichier `airbnb.duckdb`.

### 4. Lancer le pipeline complet

```bash
# Étape par étape
make run-bronze   # Ingestion couche Bronze
make run-silver   # Transformation couche Silver
make run-gold     # Calcul couche Gold

# Ou tout d'un coup
make run-all
```

### 5. Exécuter les tests qualité

```bash
make test
# ou
dbt test
```

### 6. Lancer l'application Streamlit

```bash
make app
# ou
streamlit run streamlit/app.py
```

### 7. Consulter la documentation dbt

```bash
make docs
# Ouvre automatiquement http://localhost:8080
```

---

## 📊 Fonctionnalités de l'application

### Filtres dynamiques (sidebar)
- Type de logement (room_type)
- Statut de l'hôte (superhost / standard / tous)
- Année des avis
- Catégorie de prix (Budget / Standard / Premium / Luxury)

### Onglet 🏘️ Logements
- Répartition par type de logement (pie chart)
- Logements par catégorie de prix (bar chart coloré)
- Distribution des prix (histogramme)

### Onglet 👤 Hôtes
- Proportion Superhost vs Standard
- Scatter plot performance (avis × taux positif × nb listings)
- Top 10 hôtes par satisfaction

### Onglet 💬 Avis clients
- Distribution des sentiments (positif / négatif / neutre)
- Évolution temporelle des avis
- Recherche par nom de reviewer

### Onglet 🌕 Pleine lune
- Comparaison sentiment pleine lune vs autres nuits
- Insight automatique sur l'impact calculé
- Export des données brutes

---

## 🧪 Tests qualité dbt

| Test | Modèle | Colonne | Type |
|---|---|---|---|
| not_null | bronze_hosts | id | Intégrité |
| unique | bronze_listings | id | Unicité |
| not_null + unique | bronze_full_moon_dates | full_moon_date | Intégrité |
| accepted_values | silver_reviews | sentiment | Conformité |
| relationships | silver_listings | host_id → silver_hosts | Référentiel |
| accepted_values | dim_listings | price_category | Conformité |

---

## 📁 Structure du projet

```
airbnb-analytics/
├── models/
│   ├── bronze/          # Ingestion brute (read_csv_auto)
│   │   ├── bronze_hosts.sql
│   │   ├── bronze_reviews.sql
│   │   ├── bronze_listings.sql
│   │   ├── bronze_full_moon_dates.sql
│   │   └── schema.yml
│   ├── silver/          # Nettoyage & typage
│   │   ├── silver_hosts.sql
│   │   ├── silver_listings.sql
│   │   ├── silver_reviews.sql
│   │   ├── silver_full_moon_dates.sql
│   │   └── schema.yml
│   └── gold/            # Data products
│       ├── dim_hosts.sql
│       ├── dim_listings.sql
│       ├── fact_reviews.sql
│       ├── mart_full_moon_analysis.sql
│       ├── mart_host_performance.sql
│       └── schema.yml
├── streamlit/
│   └── app.py           # Dashboard Streamlit
├── dbt_project.yml      # Configuration dbt
├── profiles.yml         # Profil DuckDB
├── requirements.txt     # Dépendances Python
├── Makefile             # Commandes raccourcies
└── README.md            # Ce fichier
```

---

## 👥 Répartition des tâches

| Membre | Responsabilités |
|---|---|
| **[Prénom 1 NOM 1]** | Architecture dbt, couches Bronze & Silver, tests qualité, documentation |
| **[Prénom 2 NOM 2]** | Couche Gold, application Streamlit, visualisations, README |

*Branches utilisées : `feature/bronze`, `feature/silver`, `feature/gold`, `feature/streamlit` → merge via Pull Requests vers `main`.*

---

## 📬 Soumission

**Destinataire :** axel@logbrain.fr  
**Objet :** `MBAESG_EVALUATION_MANAGEMENT_OPERATIONNEL_2026`
