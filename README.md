# 🎮 Steam Data Project: Análise de Preço vs. Popularidade

Este projeto analisa o dataset [Steam Store Games](https://www.kaggle.com/datasets/nikdavis/steam-store-games) para descobrir os fatores que impulsionam o **preço** e a **popularidade** dos jogos na plataforma, revelando a dicotomia central do mercado.

O projeto utiliza um pipeline completo de Data Science, incluindo limpeza de dados, engenharia de features, e três modelos de machine learning (Regressão, Classificação e Clusterização) para segmentar o mercado.

## 🚀 Demonstração


[**Assista ao vídeo de demonstração no YouTube**](https://youtu.be/mC6Hi5BFTfo)


## 💡 Conclusão Principal: A Dicotomia do Mercado

A análise revela que o sucesso de preço e o sucesso de popularidade são impulsionados por fatores completamente diferentes:

### 1. Preço é Impulsionado pela Qualidade (Regressão)
O modelo de regressão (RandomForest, R² ~77%) provou que o preço de um jogo é previsto principalmente por métricas de **qualidade e volume de conteúdo**:
* **`positive_ratings`** (Qualidade percebida)
* **`average_playtime_hours`** (Volume de conteúdo)

**Conclusão:** Para justificar um preço alto, um jogo precisa ser bom e ter muito conteúdo.

### 2. Popularidade é Impulsionada pelo Acesso (Classificação)
O modelo de classificação (DecisionTree) mostrou que para um jogo se tornar um "Hit" (top 25% mais jogado), os fatores mais importantes são:
* **`is_free`** (Ser gratuito)
* **`is_multiplayer`** (Ter funcionalidade social)

**Conclusão:** A popularidade em massa não vem da qualidade intrínseca, mas sim da remoção de barreiras (preço zero) e do efeito de rede (jogar com amigos).

### 3. O Mercado não é Monolítico (Clusterização)
O modelo K-Means (validado com Análise de Silhueta) identificou pelo menos quatro segmentos de mercado (personas) distintos, como "AAA", "Indie", "Mid-Market" e "F2P", cada um com sua própria estratégia de sucesso.

## 🛠️ Como Executar Localmente

Siga os passos para rodar a aplicação Streamlit na sua máquina.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/jotaven/steam-data-project.git](https://github.com/jotaven/steam-data-project.git)
cd steam-data-project