import streamlit as st
import pandas as pd
from collections import Counter

# ==============================
# CONFIGURAÇÃO INICIAL
# ==============================
st.set_page_config(page_title="Steam Games Analysis", layout="wide")
st.title("📊 Steam Games Dataset Explorer")

# ==============================
# CARREGAR OS DADOS
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/steam_cleaned.csv")

    # Converter release_date para datetime, se existir
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df

df = load_data()

# ==============================
# MENU LATERAL
# ==============================
menu = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Home",
        "📈 Estatísticas Gerais",
        "🎮 Jogos Populares",
        "💵 Preços e Categorias",
        "👨‍💻 Desenvolvedores e Publicadoras",
        "📊 Gêneros, Categorias e Tags",
        "📅 Lançamentos por Ano",
        "⏱️ Tempo Médio de Jogo"
    ]
)

# ==============================
# HOME
# ==============================
if menu == "🏠 Home":
    st.header("Bem-vindo ao Steam Games Dataset Explorer")
    st.markdown(
        """
        Este projeto tem como objetivo **explorar e visualizar o dataset de jogos da Steam**,
        permitindo observar tendências sobre popularidade, preços, gêneros e avaliações.  
        
        ### 🔎 O que você vai encontrar:
        - Estatísticas descritivas gerais do dataset  
        - Visualizações de jogos mais populares  
        - Análise de preços, desenvolvedores, categorias e gêneros  
        - Jogos gratuitos e evolução de lançamentos por ano  
        - Tempo médio de jogo e ranking de jogos mais jogados em média  
        
        ### 📌 Insights obtidos na análise exploratória:
        - Jogos gratuitos costumam ter maior número de jogadores.  
        - Certos gêneros dominam a plataforma, como *Action* e *Indie*.  
        - A distribuição de preços é bastante assimétrica, com muitos jogos concentrados em valores baixos.  
        
        ---
        👥 **Colaboradores:**  
        - Gustavo Targino - 30283647
        - João Victor Maia Branco - 29100259
        - João Victor Nunes de Moura - 28994281
        - João Vitor Ramos Almeida - 30081939
        - Rodrigo Pereira de Almeida - 30173591
        """
    )

# ==============================
# ESTATÍSTICAS GERAIS
# ==============================
elif menu == "📈 Estatísticas Gerais":
    st.header("📈 Estatísticas Gerais do Dataset")

    st.subheader("Dimensões do dataset")
    st.write(f"{df.shape[0]} linhas e {df.shape[1]} colunas")

    st.subheader("Amostra dos dados")
    st.dataframe(df.head(10))

    st.subheader("Estatísticas descritivas")
    st.write(df.describe(include="all").transpose())

# ==============================
# JOGOS POPULARES
# ==============================
elif menu == "🎮 Jogos Populares":
    st.header("🎮 Jogos Mais Populares")

    if "positive_ratings" in df.columns and "name" in df.columns:

        # Top 10 jogos com mais avaliações positivas
        top_positive = df.sort_values("positive_ratings", ascending=False).head(10)
        st.subheader("🏆 Top 10 jogos por avaliações positivas")
        st.bar_chart(top_positive.set_index("name")["positive_ratings"])

        # Top 10 jogos com mais avaliações negativas (se existir)
        if "negative_ratings" in df.columns:
            top_negative = df.sort_values("negative_ratings", ascending=False).head(10)
            st.subheader("👎 Top 10 jogos por avaliações negativas")
            st.bar_chart(top_negative.set_index("name")["negative_ratings"])

        # Top 10 jogos mais bem avaliados proporcionalmente (positivas / total)
        if "negative_ratings" in df.columns:
            df_ratings = df.copy()
            df_ratings["total_ratings"] = df_ratings["positive_ratings"] + df_ratings["negative_ratings"]
            df_ratings = df_ratings[df_ratings["total_ratings"] > 1000]  # filtro mínimo de avaliações
            df_ratings["ratio"] = (df_ratings["positive_ratings"] / df_ratings["total_ratings"] * 100).round(2)
            top_ratio = df_ratings.sort_values("ratio", ascending=False).head(10)
            st.subheader("✅ Top 10 jogos com melhor proporção de avaliações positivas (%)")
            st.bar_chart(top_ratio.set_index("name")["ratio"])

        # Tabela detalhada dos jogos mais populares (combinação de métricas)
        st.subheader("📋 Detalhes dos 20 jogos mais populares (avaliados)")
        top_detailed = df.sort_values("positive_ratings", ascending=False).head(20)
        cols = ["name", "positive_ratings"]
        if "negative_ratings" in df.columns:
            cols.append("negative_ratings")
        if "owners" in df.columns:
            cols.append("owners")
        st.dataframe(top_detailed[cols])

    else:
        st.warning("Colunas necessárias (`positive_ratings`, `name`) não encontradas no dataset.")


# ==============================
# PREÇOS E CATEGORIAS
# ==============================
elif menu == "💵 Preços e Categorias":
    st.header("💵 Distribuição de Preços e Categorias")

    if "price" in df.columns:
        st.subheader("Distribuição de preços (até $100)")
        free_games = (df["price"] == 0).sum()
        st.subheader(f"Quantidade de jogos gratuitos: {free_games}")
        st.bar_chart(df[df["price"] < 100]["price"].value_counts().sort_index())

        if "release_date" in df.columns:
            st.subheader("Preço médio por ano de lançamento")
            df["release_year"] = df["release_date"].dt.year
            avg_price_per_year = (
                df[df["price"] < 200]  
                .groupby("release_year")["price"]
                .mean()
                .reset_index()
            )
            st.line_chart(avg_price_per_year.set_index("release_year"))
        else:
            st.warning("Coluna `release_date` não encontrada ou não está em formato datetime.")

    if "genres" in df.columns:
        st.subheader("Top 10 gêneros mais comuns")
        genres_series = df["genres"].dropna().str.split(";").explode()
        top_genres = genres_series.value_counts().head(10)
        st.bar_chart(top_genres)



# ==============================
# DESENVOLVEDORES E PUBLICADORAS
# ==============================
elif menu == "👨‍💻 Desenvolvedores e Publicadoras":
    st.header("👨‍💻 Top Desenvolvedores e Publicadoras")

    if "developer" in df.columns and "publisher" in df.columns:
        top_devs = df["developer"].value_counts().head(10)
        top_pubs = df["publisher"].value_counts().head(10)

        st.subheader("Top 10 Desenvolvedores")
        st.bar_chart(top_devs)

        st.subheader("Top 10 Publicadoras")
        st.bar_chart(top_pubs)
    else:
        st.warning("Colunas necessárias (`developer`, `publisher`) não encontradas no dataset.")

# ==============================
# GÊNEROS, CATEGORIAS E TAGS
# ==============================
elif menu == "📊 Gêneros, Categorias e Tags":
    st.header("📊 Análise de Gêneros, Categorias e Tags")

    def contar_valores(coluna):
        lista = df[coluna].dropna().astype(str).str.split(";").sum()
        return Counter(lista).most_common(15)

    if "genres" in df.columns:
        top_genres = contar_valores("genres")
        df_genres = pd.DataFrame(top_genres, columns=["Gênero", "Frequência"]).set_index("Gênero")
        st.subheader("Top 15 Gêneros")
        st.bar_chart(df_genres)

    if "categories" in df.columns:
        top_categories = contar_valores("categories")
        df_categories = pd.DataFrame(top_categories, columns=["Categoria", "Frequência"]).set_index("Categoria")
        st.subheader("Top 15 Categorias")
        st.bar_chart(df_categories)

    if "steamspy_tags" in df.columns:
        top_tags = contar_valores("steamspy_tags")
        df_tags = pd.DataFrame(top_tags, columns=["Tag", "Frequência"]).set_index("Tag")
        st.subheader("Top 15 Tags")
        st.bar_chart(df_tags)


# ==============================
# LANÇAMENTOS POR ANO
# ==============================
elif menu == "📅 Lançamentos por Ano":
    st.header("📅 Quantidade de Jogos Lançados por Ano")

    if "release_date" in df.columns:
        df["release_year"] = df["release_date"].dt.year
        games_per_year = df["release_year"].value_counts().sort_index()

        # Gráfico geral de lançamentos por ano
        st.subheader("📈 Total de jogos lançados por ano")
        st.line_chart(games_per_year)

        # Lançamentos por categoria
        if "categories" in df.columns:
            st.subheader("📊 Lançamentos por ano e categoria (Top 5 categorias)")
            categories_series = df.dropna(subset=["categories"]).copy()
            categories_series["main_category"] = categories_series["categories"].str.split(";").str[0]
            top_cats = categories_series["main_category"].value_counts().head(5).index
            cat_per_year = (
                categories_series[categories_series["main_category"].isin(top_cats)]
                .groupby(["release_year", "main_category"])
                .size()
                .unstack(fill_value=0)
            )
            st.line_chart(cat_per_year)

        # Lançamentos por publicadora
        if "publisher" in df.columns:
            st.subheader("🏢 Lançamentos por ano e publicadora (Top 5)")
            top_pubs = df["publisher"].value_counts().head(5).index
            pub_per_year = (
                df[df["publisher"].isin(top_pubs)]
                .groupby(["release_year", "publisher"])
                .size()
                .unstack(fill_value=0)
            )
            st.line_chart(pub_per_year)

    else:
        st.warning("Coluna `release_date` não encontrada ou não é datetime.")


# ==============================
# TEMPO MÉDIO DE JOGO
# ==============================
elif menu == "⏱️ Tempo Médio de Jogo":
    st.header("⏱️ Distribuição do Tempo Médio de Jogo")

    if "average_playtime" in df.columns and "name" in df.columns and "positive_ratings" in df.columns:
        # Ranking por horas jogadas em média
        st.subheader("🏆 Top 10 Jogos por Tempo Médio (em horas)")
        df_hours = df.copy()
        df_hours["average_hours"] = (df_hours["average_playtime"] / 60).round(2)
        top_played = df_hours.sort_values("average_hours", ascending=False).head(10)
        st.dataframe(top_played[["name", "average_hours"]])

        # Ranking ponderado (tempo médio * número de avaliações positivas)
        st.subheader("🔥 Top 10 Jogos Ponderados (Tempo Médio × Avaliações Positivas)")
        df_hours["weighted_score"] = df_hours["average_playtime"] * df_hours["positive_ratings"]
        top_weighted = df_hours.sort_values("weighted_score", ascending=False).head(10)
        st.dataframe(top_weighted[["name", "average_hours", "positive_ratings", "weighted_score"]])

    else:
        st.warning("Colunas necessárias (`average_playtime`, `name`, `positive_ratings`) não encontradas no dataset.")
