import streamlit as st
import pandas as pd

st.set_page_config(page_title="Steam Games Analysis", layout="wide")

st.title("📊 Steam Games Dataset Explorer")

df = pd.read_csv("data/processed/steam_cleaned.csv")

df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["release_year"] = df["release_date"].dt.year
df["is_popular"] = df["positive_ratings"] > 5000
df["price_category"] = pd.cut(
    df["price"],
    bins=[-1, 0, 20, 60, 200],
    labels=["Free", "Cheap", "Standard", "Premium"]
)

popular_games = df[df["is_popular"]]
free_games = df[df["price"] == 0]
avg_price_per_year = df.groupby("release_year")["price"].mean().reset_index()

st.subheader("🔎 Dataset original com novas colunas")
st.dataframe(df.head())

st.subheader("🔥 Jogos Populares")
st.dataframe(popular_games.head())

st.subheader("🎮 Jogos Grátis")
st.dataframe(free_games.head())

st.subheader("💰 Preço médio por ano")
st.line_chart(avg_price_per_year.set_index("release_year"))
