import streamlit as st
import joblib
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import os

# -----------------
# Configuração da Página
# -----------------
st.set_page_config(
    page_title="Análise de Mercado - Steam",
    page_icon="🎮",
    layout="wide",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(APP_DIR, '..', 'models')
# -----------------

# -----------------
# Carregar Modelos (uma única vez)
# -----------------
@st.cache_resource
def load_models():
    """Carrega os modelos e o gráfico do disco."""
    try:
        models = {
            "regressor_preco": joblib.load(os.path.join(MODELS_DIR, 'modelo_regressao_preco.joblib')),
            "scaler_regressao": joblib.load(os.path.join(MODELS_DIR, 'scaler_regressao.joblib')),
            "classificador_hit": joblib.load(os.path.join(MODELS_DIR, 'modelo_classificacao_hit.joblib')),
        }
        with open(os.path.join(MODELS_DIR, 'pca_cluster_plot.html'), 'r', encoding='utf-8') as f:
            models["pca_html"] = f.read()
            
        return models
    except FileNotFoundError:
        st.error("Erro: Arquivos de modelo não encontrados. Execute os notebooks para gerar os modelos.")
        return None

models = load_models()

# -----------------
# Barra Lateral (Navegação)
# -----------------
st.sidebar.title("🎮 Análise Steam")
st.sidebar.markdown("Navegue pelas descobertas do projeto:")
page = st.sidebar.radio(
    "Escolha a Análise:",
    ("Conclusão Principal", "Previsão de Preço (Regressão)", "Previsão de 'Hit' (Classificação)", "Segmentos de Mercado (Cluster)")
)

# --- MUDANÇA: Colaboradores movidos para a sidebar ---
st.sidebar.markdown("---") # Linha divisória
st.sidebar.markdown(
    """
    👥 **Colaboradores:**
    - Gustavo Targino - 30283647
    - João Victor Maia Branco - 29100259
    - João Victor Nunes de Moura - 28994281
    - João Vitor Ramos Almeida - 30081939
    - Rodrigo Pereira de Almeida - 30173591
    """
)
# -----------------

# -----------------
# Página 1: Conclusão Principal
# -----------------
if page == "Conclusão Principal":
    st.title("💡 Conclusão Principal: A Dicotomia do Mercado Steam")
    st.markdown("""
    Este projeto revela a dinâmica central do mercado de jogos na Steam:
    
    1.  **O Preço é impulsionado pela QUALIDADE.**
    2.  **A Popularidade ('Hit') é impulsionada pelo ACESSO.**
    
    ---
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 1. Preço é movido por Qualidade e Conteúdo")
        st.markdown("""
        O modelo de **Regressão** (com R² de ~77%) prova que o preço de um jogo é
        altamente previsível com base em métricas de qualidade:
        
        * **`positive_ratings`** (Avaliações Positivas)
        * **`average_playtime_hours`** (Tempo Médio de Jogo)
        
        **Conclusão:** Jogos caros precisam justificar seu preço com alta qualidade e muito conteúdo.
        """)

    with col2:
        st.warning("### 2. Popularidade é movida por Acesso e Rede")
        st.markdown("""
        O modelo de **Classificação** mostra que para se tornar um "Hit" (top 25% em popularidade),
        qualidade não é o fator principal. Os drivers são:
        
        * **`is_free`** (Ser Gratuito)
        * **`is_multiplayer`** (Ter modo Multi-player)
        
        **Conclusão:** O sucesso em massa é uma questão de remover barreiras (preço zero) e
        criar efeitos de rede (jogar com amigos).
        """)

# -----------------
# Página 2: Previsão de Preço (Regressão)
# -----------------
elif page == "Previsão de Preço (Regressão)" and models:
    st.title("💰 Previsor de Preço (Regressão)")
    st.markdown("Use o modelo para estimar o preço de um jogo com base em suas métricas de qualidade. **(Modelo treinado apenas em jogos pagos)**")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            positive_ratings = st.number_input("Total de Avaliações Positivas", min_value=1, value=10000, step=1000)
        with col2:
            average_playtime_hours = st.number_input("Tempo Médio de Jogo (Horas)", min_value=1.0, value=50.0, step=5.0)
        with col3:
            total_ratings = st.number_input("Total de Avaliações (Positivas + Negativas)", min_value=1, value=12000, step=1000)

    reg_feature_names = ['positive_ratings', 'average_playtime_hours', 'total_ratings']
    data = [[positive_ratings, average_playtime_hours, total_ratings]]

    features_df = pd.DataFrame(data, columns=reg_feature_names)

    # Aplicar o scaler  
    features_scaled = models["scaler_regressao"].transform(features_df)
    # Fazer a predição
    pred_log = models["regressor_preco"].predict(features_scaled)
    pred_price = np.expm1(pred_log)[0] # Reverter o log

    st.subheader(f"Preço Previsto: ${pred_price:.2f}")

# -----------------
# Página 3: Previsão de 'Hit' (Classificação)
# -----------------
elif page == "Previsão de 'Hit' (Classificação)" and models:
    st.title("🔥 Previsor de 'Hit' (Classificação)")
    st.markdown("Use o modelo (Decision Tree) para prever a chance de um jogo se tornar um 'Hit' (top 25% em popularidade).")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            is_free = st.toggle("É Gratuito (Free-to-Play)?", value=True)
            is_multiplayer = st.toggle("É Multi-player?", value=True)
        
        with col2:
            price = st.number_input("Preço (USD)", min_value=0.0, value=0.0, step=5.0, disabled=is_free)
            average_playtime_hours = st.number_input("Tempo Médio de Jogo (Horas)", min_value=0.0, value=10.0, step=5.0)
            positive_ratings = st.number_input("Total de Avaliações Positivas", min_value=0, value=1000, step=100)

    is_free_int = 1 if is_free else 0
    is_multiplayer_int = 1 if is_multiplayer else 0
    price_val = 0.0 if is_free else price

    clf_feature_names = ['is_free', 'is_multiplayer', 'price', 'average_playtime_hours', 'positive_ratings']
    data = [[is_free_int, is_multiplayer_int, price_val, average_playtime_hours, positive_ratings]]

    features_df = pd.DataFrame(data, columns=clf_feature_names)

    prediction = models["classificador_hit"].predict(features_df)[0]
    probability = models["classificador_hit"].predict_proba(features_df)[0]

    if prediction == 1:
        st.success(f"**É um HIT!** (Probabilidade: {probability[1]:.1%})")
        st.image("https://media.tenor.com/POKm-vP3ZJQAAAAC/pepe-dance.gif", width=150)
    else:
        st.error(f"**Não é um Hit.** (Probabilidade: {probability[0]:.1%})")

# -----------------
# Página 4: Segmentos de Mercado (Cluster)
# -----------------
elif page == "Segmentos de Mercado (Cluster)" and models:
    st.title("📊 Segmentos de Mercado (Clusterização)")
    st.markdown("""
    O modelo K-Means identificou 4 segmentos de mercado distintos (Personas).
    O gráfico PCA abaixo visualiza esses clusters no espaço 2D.
    """)
    
    components.html(models["pca_html"], height=600, scrolling=True)