import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Dashboard Hébergements", layout="wide")

# -----------------------
# STYLE
# -----------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.kpi-card {
    background: linear-gradient(135deg, #ff5a5f, #ff9966);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏨 Dashboard Hébergements Touristiques")

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    all_data = []
    for offset in range(0, 1000, 100):
        res = requests.get(f"{API_URL}/hebergements?limit=100&offset={offset}")
        if res.status_code == 200:
            all_data.extend(res.json())
    return pd.DataFrame(all_data)

df = load_data()

if df.empty:
    st.error("❌ Aucune donnée récupérée")
    st.stop()

# -----------------------
# CLEAN TYPES
# -----------------------
df["capacite"] = pd.to_numeric(df["capacite"], errors="coerce").fillna(0)
df["nb_etoiles"] = pd.to_numeric(df["nb_etoiles"], errors="coerce").fillna(0)
df["nb_chambres"] = pd.to_numeric(df["nb_chambres"], errors="coerce").fillna(0)

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.header("🔎 Filtres")

types = st.sidebar.multiselect(
    "Type d’hébergement",
    sorted(df["type_hebergement"].dropna().unique())
)

communes = st.sidebar.multiselect(
    "Commune",
    sorted(df["commune"].dropna().unique())
)

min_star = int(df["nb_etoiles"].min())
max_star = int(df["nb_etoiles"].max())

stars_range = st.sidebar.slider(
    "Nombre d’étoiles",
    min_value=min_star,
    max_value=max_star,
    value=(min_star, max_star)
)

# -----------------------
# FILTER
# -----------------------
filtered_df = df.copy()

if types:
    filtered_df = filtered_df[filtered_df["type_hebergement"].isin(types)]

if communes:
    filtered_df = filtered_df[filtered_df["commune"].isin(communes)]

filtered_df = filtered_df[
    (filtered_df["nb_etoiles"] >= stars_range[0]) &
    (filtered_df["nb_etoiles"] <= stars_range[1])
]

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏆 Top & Ranking", "📈 Analyse avancée"])

# =====================================================
# 🟢 TAB 1 : DASHBOARD
# =====================================================
with tab1:

    st.subheader("📌 Indicateurs clés")

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="kpi-card"><h2>{len(filtered_df)}</h2><p>Hébergements</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi-card"><h2>{int(filtered_df["capacite"].sum())}</h2><p>Capacité</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="kpi-card"><h2>{round(filtered_df["nb_etoiles"].mean(),2)}</h2><p>Étoiles moyennes</p></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="kpi-card"><h2>{int(filtered_df["nb_chambres"].sum())}</h2><p>Chambres</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    top_communes = filtered_df.groupby("commune").size().reset_index(name="count").sort_values("count", ascending=False).head(10)
    fig1 = px.bar(top_communes, x="commune", y="count", title="Top 10 communes", color="count")
    col1.plotly_chart(fig1, use_container_width=True)

    type_chart = filtered_df.groupby("type_hebergement").size().reset_index(name="count")
    fig2 = px.pie(type_chart, names="type_hebergement", values="count", title="Répartition des types")
    col2.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)

    star_chart = filtered_df.groupby("nb_etoiles").size().reset_index(name="count")
    fig3 = px.bar(star_chart, x="nb_etoiles", y="count", title="Distribution étoiles", color="count")
    col1.plotly_chart(fig3, use_container_width=True)

    fig4 = px.histogram(filtered_df, x="capacite", nbins=30, title="Distribution capacité")
    col2.plotly_chart(fig4, use_container_width=True)

# =====================================================
# 🟡 TAB 2 : TOP / SCORE
# =====================================================
with tab2:

    st.subheader("🏆 Classement intelligent")

    st.markdown("""
    👉 Score basé sur :
    - 70% capacité
    - 30% qualité (étoiles)
    """)

    filtered_df["score"] = (
        filtered_df["capacite"] * 0.7 +
        filtered_df["nb_etoiles"] * 50
    )

    top_df = filtered_df.sort_values("score", ascending=False).head(10)

    st.dataframe(
        top_df[["nom", "commune", "capacite", "nb_etoiles", "score"]],
        use_container_width=True
    )

    # Graph TOP
    fig_top = px.bar(
        top_df,
        x="nom",
        y="score",
        color="score",
        title="Top 10 hébergements (score)"
    )
    st.plotly_chart(fig_top, use_container_width=True)

# =====================================================
# 🔵 TAB 3 : ANALYSE AVANCÉE
# =====================================================
with tab3:

    st.subheader("📊 Analyse avancée")

    col1, col2 = st.columns(2)

    cap_type = df.groupby("type_hebergement")["capacite"].sum().reset_index()
    fig5 = px.bar(cap_type, x="type_hebergement", y="capacite", title="Capacité par type")
    col1.plotly_chart(fig5, use_container_width=True)

    fig6 = px.scatter(df, x="nb_etoiles", y="capacite", title="Étoiles vs capacité")
    col2.plotly_chart(fig6, use_container_width=True)

    col1, col2 = st.columns(2)

    fig7 = px.histogram(df, x="nb_chambres", title="Distribution chambres")
    col1.plotly_chart(fig7, use_container_width=True)

    fig8 = px.box(df, x="type_hebergement", y="nb_etoiles", title="Étoiles par type")
    col2.plotly_chart(fig8, use_container_width=True)
