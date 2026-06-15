"""
Airbnb Analytics Platform — Streamlit Dashboard
MBA ESG Paris — Promotion 2026
"""
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Airbnb Analytics Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = Path(__file__).parent.parent / "airbnb.duckdb"

@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH), read_only=True)

def query(sql: str) -> pd.DataFrame:
    return get_connection().execute(sql).df()

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🏠 Airbnb Analytics Platform")
st.markdown("*Analyse des logements, hôtes, avis clients et impact des nuits de pleine lune.*")
st.divider()

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🎛️ Filtres")
    room_types = query("SELECT DISTINCT room_type FROM main_gold.dim_listings ORDER BY room_type")
    rt_opts = ["Tous"] + room_types["room_type"].dropna().tolist()
    sel_rt = st.selectbox("Type de logement", rt_opts)

    superhost_f = st.radio("Hôte", ["Tous", "Superhost uniquement", "Non-superhost"])

    years = query("SELECT DISTINCT review_year FROM main_gold.fact_reviews WHERE review_year IS NOT NULL ORDER BY review_year")
    yr_opts = ["Toutes"] + [str(int(y)) for y in years["review_year"].tolist()]
    sel_yr = st.selectbox("Année des avis", yr_opts)

    price_cats = ["Toutes", "Budget", "Standard", "Premium", "Luxury"]
    sel_pc = st.selectbox("Catégorie de prix", price_cats)

    st.divider()
    st.caption("MBA ESG — Promotion 2026")

# ── Build WHERE ──────────────────────────────────────────────────────────────
w = []
if sel_rt != "Tous":       w.append(f"room_type = '{sel_rt}'")
if superhost_f == "Superhost uniquement": w.append("is_superhost = TRUE")
elif superhost_f == "Non-superhost":       w.append("is_superhost = FALSE")
if sel_yr != "Toutes":     w.append(f"review_year = {sel_yr}")
if sel_pc != "Toutes":     w.append(f"price_category = '{sel_pc}'")
where = ("WHERE " + " AND ".join(w)) if w else ""

# ── KPIs ────────────────────────────────────────────────────────────────────
kpi = query(f"""
    SELECT COUNT(DISTINCT listing_id) AS nb_listings,
           COUNT(DISTINCT host_id)    AS nb_hosts,
           COUNT(*)                   AS nb_reviews,
           ROUND(AVG(price), 2)       AS avg_price,
           SUM(CASE WHEN is_full_moon THEN 1 ELSE 0 END) AS full_moon_reviews
    FROM main_gold.fact_reviews {where}
""").iloc[0]

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("🏘️ Logements", f"{int(kpi['nb_listings']):,}")
c2.metric("👤 Hôtes", f"{int(kpi['nb_hosts']):,}")
c3.metric("💬 Avis", f"{int(kpi['nb_reviews']):,}")
c4.metric("💰 Prix moyen", f"${kpi['avg_price']:.0f}")
c5.metric("🌕 Avis pleine lune", f"{int(kpi['full_moon_reviews']):,}")
st.divider()

# ── Tabs ────────────────────────────────────────────────────────────────────
t1,t2,t3,t4 = st.tabs(["🏘️ Logements","👤 Hôtes","💬 Avis clients","🌕 Pleine lune"])

with t1:
    st.subheader("Analyse des logements")
    ca, cb = st.columns(2)
    with ca:
        df = query("SELECT room_type, COUNT(*) AS nb FROM main_gold.dim_listings GROUP BY room_type ORDER BY nb DESC")
        st.plotly_chart(px.pie(df, names="room_type", values="nb",
            title="Répartition par type de logement",
            color_discrete_sequence=px.colors.qualitative.Set2), use_container_width=True)
    with cb:
        df = query("SELECT price_category, COUNT(*) AS nb, ROUND(AVG(price),2) AS avg_price FROM main_gold.dim_listings GROUP BY price_category ORDER BY avg_price")
        st.plotly_chart(px.bar(df, x="price_category", y="nb", color="avg_price",
            color_continuous_scale="Blues", title="Logements par catégorie de prix",
            labels={"nb":"Nombre","price_category":"Catégorie","avg_price":"Prix moyen ($)"}), use_container_width=True)
    df = query("SELECT price FROM main_gold.dim_listings WHERE price < 1000")
    st.plotly_chart(px.histogram(df, x="price", nbins=60, title="Distribution des prix",
        color_discrete_sequence=["#FF5A5F"], labels={"price":"Prix ($)"}), use_container_width=True)

with t2:
    st.subheader("Analyse des hôtes")
    ca, cb = st.columns(2)
    with ca:
        df = query("SELECT CASE WHEN is_superhost THEN 'Superhost' ELSE 'Standard' END AS type_hote, COUNT(*) AS nb FROM main_gold.dim_hosts GROUP BY is_superhost")
        st.plotly_chart(px.pie(df, names="type_hote", values="nb", title="Superhost vs Standard",
            color_discrete_map={"Superhost":"#FF5A5F","Standard":"#767676"}), use_container_width=True)
    with cb:
        df = query("SELECT host_name, nb_listings, total_reviews, positive_rate_pct, is_superhost FROM main_gold.mart_host_performance WHERE total_reviews >= 5 ORDER BY positive_rate_pct DESC LIMIT 20")
        st.plotly_chart(px.scatter(df, x="total_reviews", y="positive_rate_pct",
            size="nb_listings", color="is_superhost", hover_name="host_name",
            title="Performance des hôtes (top 20)",
            labels={"total_reviews":"Nb avis","positive_rate_pct":"% positifs"}), use_container_width=True)
    st.subheader("🏆 Top 10 hôtes")
    df = query("SELECT host_name, CASE WHEN is_superhost THEN '⭐ Superhost' ELSE 'Standard' END AS statut, nb_listings, total_reviews, positive_rate_pct FROM main_gold.mart_host_performance ORDER BY positive_reviews DESC LIMIT 10")
    st.dataframe(df, use_container_width=True, hide_index=True)

with t3:
    st.subheader("Analyse des avis clients")
    ca, cb = st.columns(2)
    with ca:
        df = query(f"SELECT sentiment, COUNT(*) AS nb FROM main_gold.fact_reviews {where} GROUP BY sentiment ORDER BY nb DESC")
        cmap = {"positive":"#00A699","negative":"#FF5A5F","neutral":"#767676"}
        st.plotly_chart(px.bar(df, x="sentiment", y="nb", color="sentiment",
            color_discrete_map=cmap, title="Distribution des sentiments",
            labels={"nb":"Nb avis","sentiment":"Sentiment"}), use_container_width=True)
    with cb:
        df = query(f"SELECT review_year, review_month, COUNT(*) AS nb FROM main_gold.fact_reviews {where} GROUP BY review_year, review_month ORDER BY review_year, review_month")
        if not df.empty:
            df["period"] = df["review_year"].astype(int).astype(str) + "-" + df["review_month"].astype(int).astype(str).str.zfill(2)
            st.plotly_chart(px.line(df, x="period", y="nb", title="Évolution des avis",
                labels={"nb":"Nb avis","period":"Période"}), use_container_width=True)
    reviewer_input = st.text_input("🔍 Rechercher par nom de reviewer")
    if reviewer_input:
        df = query(f"SELECT reviewer_name, review_date, listing_name, review_text, sentiment FROM main_gold.fact_reviews WHERE LOWER(reviewer_name) LIKE LOWER('%{reviewer_input}%') ORDER BY review_date DESC LIMIT 50")
        st.dataframe(df, use_container_width=True, hide_index=True)

with t4:
    st.subheader("🌕 Impact des nuits de pleine lune")
    df = query("SELECT CASE WHEN is_full_moon THEN '🌕 Pleine lune' ELSE '🌑 Autre nuit' END AS nuit, sentiment, nb_reviews, pct_sentiment FROM main_gold.mart_full_moon_analysis")
    ca, cb = st.columns(2)
    with ca:
        st.plotly_chart(px.bar(df, x="sentiment", y="nb_reviews", color="nuit", barmode="group",
            title="Sentiments : Pleine lune vs Autre nuit",
            color_discrete_map={"🌕 Pleine lune":"#FFC107","🌑 Autre nuit":"#455A64"},
            labels={"nb_reviews":"Nb avis"}), use_container_width=True)
    with cb:
        st.plotly_chart(px.bar(df, x="nuit", y="pct_sentiment", color="sentiment", barmode="stack",
            title="Répartition (%) sentiments par type de nuit",
            color_discrete_map={"positive":"#00A699","negative":"#FF5A5F","neutral":"#767676"},
            labels={"pct_sentiment":"% des avis"}), use_container_width=True)
    df_i = query("SELECT is_full_moon, ROUND(SUM(CASE WHEN sentiment='positive' THEN nb_reviews ELSE 0 END)*100.0/SUM(nb_reviews),1) AS pct_pos, ROUND(SUM(CASE WHEN sentiment='negative' THEN nb_reviews ELSE 0 END)*100.0/SUM(nb_reviews),1) AS pct_neg FROM main_gold.mart_full_moon_analysis GROUP BY is_full_moon")
    if len(df_i) == 2:
        fm = df_i[df_i["is_full_moon"] == True]
        ot = df_i[df_i["is_full_moon"] == False]
        if not fm.empty and not ot.empty:
            diff = fm.iloc[0]["pct_pos"] - ot.iloc[0]["pct_pos"]
            st.info(f"{'📈' if diff>0 else '📉'} Pleine lune : **{fm.iloc[0]['pct_pos']}%** d'avis positifs vs **{ot.iloc[0]['pct_pos']}%** les autres nuits ({'+'if diff>0 else ''}{diff:.1f} pts).")
    st.dataframe(df, use_container_width=True, hide_index=True)
