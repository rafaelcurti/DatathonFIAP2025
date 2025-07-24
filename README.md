# Decision.AI – Recomendação Inteligente de Candidatos

Este projeto foi desenvolvido como parte do Datathon da FIAP, com o objetivo de otimizar o processo de recrutamento da empresa **Decision** — especializada em bodyshop e alocação de profissionais de TI. Utilizamos **inteligência artificial** para recomendar os candidatos com maior compatibilidade para cada vaga.

## 🚀 Funcionalidades

- 🔎 Análise de currículo com processamento de linguagem natural (NLP)
- 🧠 Recomendação de candidatos baseada em similaridade textual (TF-IDF + SVD)
- ✅ Filtro por nível de match e quantidade de candidatos
- 📊 Dashboards interativos com métricas e distribuição por áreas
- 🔄 Armazenamento local de candidatos para futuras buscas
- 📌 Identificação de perfis com maior chance de contratação com base em histórico

## 🧰 Tecnologias Utilizadas

- Python 3.11
- Streamlit
- Scikit-learn (TF-IDF, SVD, LightGBM)
- Pandas / Numpy
- Matplotlib / Plotly
- Git / GitHub
- Docker (opcional)

## 📁 Estrutura do Projeto

```
decision_ai/
│
├── app/                        # Aplicação principal em Streamlit
│   ├── main.py                 # Interface principal
│   ├── data_preparation.py     # Funções de carregamento e transformação
│   └── utils/                  # Scripts auxiliares
│
├── data/                       # Dados originais do desafio
│   ├── applicants_part_1.json
│   ├── applicants_part_2.json
│   ├── applicants_part_3.json
│   ├── jobs.json
│   └── prospects.json
│
├── models/                     # Modelos de ML treinados (.pkl)
│
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

## 🏁 Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/decision_ai.git
   cd decision_ai
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate   # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o app:
   ```bash
   streamlit run app/main.py
   ```

## 🧪 Testes e Validação

O modelo foi treinado com histórico de contratações reais, com balanceamento de classes e validação cruzada. Métricas como acurácia e F1-score foram utilizadas para avaliar os modelos.

## 🤝 Colaboradores

  - Ozir José Azevedo Junior 
  - Paloma Cristina Pinheiro
  - Rafael Curti Barros
  - Rilciane de Sousa Bezerra

## 📌 Observações

- A base `applicants.json` foi dividida em 3 partes para viabilizar o versionamento no GitHub.
- Perfis considerados como "positivos" para o treinamento incluem: `Contratado pela Decision`, `Proposta Aceita`, `Aprovado`, `Contratado como Hunting`, `Desistiu da Contratação`.

## 📝 Licença

Este projeto é apenas para fins educacionais e de demonstração. Todos os dados foram fornecidos exclusivamente para uso no Datathon FIAP 2025.
