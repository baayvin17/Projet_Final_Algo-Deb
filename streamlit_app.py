import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Dashboard Tips", layout="wide")

st.title("📊 Dashboard Analyse des Tips (Restaurants)")

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    res = requests.get(f"{API_URL}/tips?limit=500")
    data = res.json()
    return pd.DataFrame(data)

df = load_data()

# -----------------------
# SIDEBAR FILTRES
# -----------------------
st.sidebar.header("🔎 Filtres")

if "day" in df.columns:
    selected_days = st.sidebar.multiselect("Jour", df["day"].unique(), default=df["day"].unique())
else:
    selected_days = []

if "sex" in df.columns:
    selected_sex = st.sidebar.multiselect("Sexe", df["sex"].unique(), default=df["sex"].unique())
else:
    selected_sex = []

if "smoker" in df.columns:
    selected_smoker = st.sidebar.multiselect("Fumeur", df["smoker"].unique(), default=df["smoker"].unique())
else:
    selected_smoker = []

# -----------------------
# APPLY FILTERS
# -----------------------
filtered_df = df.copy()

if selected_days:
    filtered_df = filtered_df[filtered_df["day"].isin(selected_days)]

if selected_sex:
    filtered_df = filtered_df[filtered_df["sex"].isin(selected_sex)]

if selected_smoker:
    filtered_df = filtered_df[filtered_df["smoker"].isin(selected_smoker)]

# -----------------------
# KPIs
# -----------------------
st.subheader("📌 Indicateurs Clés")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transactions", len(filtered_df))
col2.metric("💰 Total CA", round(filtered_df["total_bill"].sum(), 2))
col3.metric("💸 Total Tips", round(filtered_df["tip"].sum(), 2))
col4.metric("📊 Tip Moyen", round(filtered_df["tip"].mean(), 2))

# -----------------------
# GRAPHS
# -----------------------
st.subheader("📈 Analyses")

col1, col2 = st.columns(2)

# Tips par jour
if "day" in filtered_df.columns:
    tips_by_day = filtered_df.groupby("day")["tip"].mean()
    col1.write("💡 Tip moyen par jour")
    col1.bar_chart(tips_by_day)

# CA par jour
if "day" in filtered_df.columns:
    ca_by_day = filtered_df.groupby("day")["total_bill"].sum()
    col2.write("💰 Chiffre d'affaires par jour")
    col2.bar_chart(ca_by_day)

# -----------------------
# ANALYSE PAR PROFIL
# -----------------------
st.subheader("👥 Analyse Clients")

col1, col2 = st.columns(2)

# Sexe
if "sex" in filtered_df.columns:
    sex_analysis = filtered_df.groupby("sex")["tip"].mean()
    col1.write("👨‍🦱 Tip moyen par sexe")
    col1.bar_chart(sex_analysis)

# Fumeur
if "smoker" in filtered_df.columns:
    smoker_analysis = filtered_df.groupby("smoker")["tip"].mean()
    col2.write("🚬 Impact du tabac sur les tips")
    col2.bar_chart(smoker_analysis)

# -----------------------
# DISTRIBUTION
# -----------------------
st.subheader("📊 Distribution")

col1, col2 = st.columns(2)

col1.write("Distribution des tips")
col1.bar_chart(filtered_df["tip"])

col2.write("Distribution des additions")
col2.bar_chart(filtered_df["total_bill"])

# -----------------------
# TABLE DETAILLEE
# -----------------------
st.subheader("📋 Données détaillées")

st.dataframe(filtered_df)
