# 🤖 Decision AI - MVP para Recrutamento Inteligente

Este projeto é um MVP (Minimum Viable Product) construído para o **Datathon da FIAP**, em parceria com a **Decision**, empresa especializada em recrutamento de profissionais de TI.

A solução utiliza **Inteligência Artificial** para **recomendar os candidatos mais aderentes às vagas disponíveis**, com base em análise de currículos e requisitos técnicos. A interface interativa foi construída com **Streamlit**, e o deploy está preparado para ser executado via **Docker**.

---

## 📌 Funcionalidades

- ✅ Ranking de candidatos por vaga com **score de aderência**
- 📊 Dashboards com indicadores gerais (nível de inglês, área de atuação, número de contratados etc.)
- 🧠 Treinamento de modelo preditivo com **LightGBM** e processamento de texto com **TF-IDF + SVD**
- 📦 Projeto preparado para execução local e em contêiner Docker

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10
- Streamlit
- Pandas
- Scikit-learn
- LightGBM
- XGBoost
- Joblib
- Matplotlib / Seaborn
- Docker

---

## 📁 Estrutura do Projeto

```
decision_mvp/
├── app/
│   ├── main.py                # Aplicação principal em Streamlit
│   ├── model_train.py         # Treinamento e salvamento do modelo
│   ├── data_preparation.py    # Tratamento e junção das bases
│   └── model.joblib           # Modelo treinado
├── data/
│   ├── applicants.json        # Base de candidatos
│   ├── jobs.json              # Base de vagas
│   ├── prospects.json         # Histórico de entrevistas
├── Dockerfile                 # Container Docker
├── requirements.txt           # Bibliotecas do Python
└── README.md                  # Este arquivo
```

---

## 🚀 Como Executar o Projeto

### 🔧 Ambiente Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd decision_ai
```

2. Crie o ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o Streamlit:
```bash
streamlit run app/main.py
```

---

### 🐳 Execução com Docker

1. **Build da imagem:**
```bash
docker build -t decision-ai
```

2. **Execute o contêiner:**
```bash
docker run -p 8501:8501 decision-ai
```

Acesse no navegador: [http://localhost:8501](http://localhost:8501)

---

## 🧠 Modelo de IA

O modelo preditivo foi treinado com dados históricos de candidatos, utilizando:
- Vetorização textual com **TF-IDF**
- Redução de dimensionalidade com **SVD**
- Classificação com **LightGBM**
- Balanceamento de classes e métricas de performance avaliadas

---

## 👨‍💼 Consultores Responsáveis

  - Ozir José Azevedo Junior 
  - Paloma Cristina Pinheiro
  - Rafael Curti Barros
  - Rilciane de Sousa Bezerra

---

## 📄 Licença

Este projeto é apenas para fins educacionais e de demonstração. Todos os dados foram fornecidos exclusivamente para uso no Datathon FIAP 2025.
