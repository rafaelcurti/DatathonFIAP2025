
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from data_preparation import merge_all
from model_train import train_model
import os

st.set_page_config(page_title="IA para Recrutamento", layout="wide")
st.title("🤖 IA para Recrutamento - Decision")

@st.cache_resource
def load_model_and_data():
    applicants_paths = [
        "data/applicants_part1.json",
        "data/applicants_part2.json",
        "data/applicants_part3.json"
    ]
    merged, applicants, jobs = merge_all(applicants_paths, "data/jobs.json", "data/prospects.json")
    if os.path.exists("app/model.joblib"):
        model, tfidf, svd_obj = joblib.load("app/model.joblib")
    else:
        model, tfidf, svd_obj = train_model(merged)
        joblib.dump((model, tfidf, svd_obj), "app/model.joblib")
    return merged, applicants, jobs, model, tfidf, svd_obj

with st.spinner("🔄 Carregando dados..."):
    merged, applicants, jobs, model, tfidf, svd_obj = load_model_and_data()
st.success("✅ Pronto!")

menu = st.sidebar.radio("Navegação", ["🏆 Ranking por Vaga", "📊 Dashboards", "👨‍💼 Consultores"])

if menu == "🏆 Ranking por Vaga":
    st.header("🎯 Ranking de Candidatos")
    import re
    jobs["titulo_limpo"] = jobs["titulo"].apply(lambda x: re.sub(r"^\d+\s*|\s*\d+$", "", str(x)).strip())

    vaga_dict = dict(zip(jobs["titulo_limpo"], jobs["job_id"]))
    
    vaga_opcoes = jobs[["job_id", "titulo_limpo"]].drop_duplicates().sort_values("titulo_limpo")
    vaga_dict = dict(zip(vaga_opcoes["titulo_limpo"], vaga_opcoes["job_id"]))
    titulo_selecionado = st.selectbox("Selecione a vaga:", options=list(vaga_dict.keys()))
    job_id = vaga_dict[titulo_selecionado]

    qtd = st.slider("Quantidade máxima de candidatos:", 1, 50, 5)
    min_score = st.slider("Score mínimo (0 a 1):", 0.0, 1.0, 0.5, step=0.01)

    job_id = vaga_dict[titulo_selecionado]
    candidatos_vaga = merged[merged["job_id"] == job_id].copy()
    candidatos_vaga = candidatos_vaga[candidatos_vaga["cv"].notna()]

    top_candidatos = pd.DataFrame()

    if candidatos_vaga.empty:
        st.warning("⚠️ Nenhum candidato possui informações de CV para essa vaga.")
    else:
        X_text = candidatos_vaga["cv"] + " " + candidatos_vaga["conhecimentos_tecnicos"].fillna("")
        if X_text.empty or all(x.strip() == "" for x in X_text):
            st.warning("⚠️ Não há informações suficientes para calcular os scores dos candidatos.")
        else:
            X_tfidf = tfidf.transform(X_text)
            X_reduzido = svd_obj.transform(X_tfidf)
            candidatos_vaga["score_match"] = model.predict_proba(X_reduzido)[:, 1]

            top_candidatos = candidatos_vaga[candidatos_vaga["score_match"] >= min_score]
            top_candidatos = top_candidatos.sort_values("score_match", ascending=False).head(qtd)

                        
    if top_candidatos.empty:
        st.warning("⚠️ Nenhum candidato atende aos critérios definidos.")
    else:
        st.markdown("ℹ️ O score representa a **probabilidade estimada de contratação**, variando de `0.0` a `1.0`. Quanto maior, melhor o match.")

        dados_export = []
        for _, row in top_candidatos.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    with st.expander(f"{row['nome']} (detalhes)"):
                        st.write(f"📧 Email: {row['email']}")
                        st.write(f"📞 Telefone: {row.get('telefone') or row.get('telefone_celular') or 'N/A' or 'N/A'}")
                        st.write(f"Área de Atuação: {row['area_atuacao'] or 'N/A'}")
                        st.write(f"Nível: {row['nivel_profissional'] or 'N/A'}")
                        st.write(f"Objetivo Profissional: {row.get('objetivo_profissional', '') or 'N/A'}")
                with col2:
                    st.metric("Score Match", f"{row['score_match']:.2%}")

            dados_export.append({
                "Nome": row["nome"],
                "Email": row["email"],
                "Telefone": row.get("telefone") or row.get("telefone_celular") or "N/A",
                "Score Match": round(row["score_match"] * 100, 2)
            })

        df_export = pd.DataFrame(dados_export)
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Ranking")
        st.download_button(
            label="📥 Baixar Ranking (Excel)",
            data=output.getvalue(),
            file_name="ranking_candidatos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

elif menu == "📊 Dashboards":
    st.header("📈 Indicadores Gerais")
    col1, col2 = st.columns(2)
    col1.metric("Total de Vagas", jobs.shape[0])
    col2.metric("Total de Candidatos", applicants.shape[0])
    contratados = merged["foi_contratado"].sum()
    st.metric("Total de Contratados (perfil positivo)", contratados)

    #st.subheader("Distribuição por Nível de Inglês")
    import matplotlib.pyplot as plt
    nivel_ingles = applicants["nivel_ingles"]
    nivel_ingles = nivel_ingles[nivel_ingles.str.strip() != ""]
    nivel_counts = nivel_ingles.value_counts()
    total = nivel_counts.sum()
    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(nivel_counts.index, nivel_counts.values, color="lightgreen")
    for bar in bars:
        height = bar.get_height()
        percent = f"{(height / total) * 100:.1f}%"
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{int(height)} ({percent})",
                ha='center', va='bottom', fontsize=9)
    ax.set_ylabel("Quantidade")
    ax.set_title("Distribuição por Nível de Inglês")
    st.pyplot(fig)

    st.markdown("  \n \n  ")
    #st.subheader("Distribuição por Área de Atuação")

    def mapear_area(area):
        area = str(area).lower()
        if "ti" in area:
            return "TI"
        elif "admin" in area:
            return "Administrativa"
        elif "finance" in area:
            return "Financeira"
        elif "comercial" in area:
            return "Comercial"
        elif "marketing" in area:
            return "Marketing"
        elif "engenharia" in area:
            return "Engenharia"
        elif "jurídico" in area or "juridico" in area:
            return "Jurídica"
        elif "rh" in area or "recursos humanos" in area:
            return "RH"
        else:
            return area.title()

    area_padronizada = applicants["area_atuacao"].map(mapear_area)
    area_counts = area_padronizada.value_counts()

    # Remove a área com maior contagem (opcional)
    area_counts = area_counts[1:]

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    bars2 = ax2.bar(area_counts.index, area_counts.values, color="skyblue")

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height + 30, f"{int(height)}",
                 ha='center', va='bottom', fontsize=9)

    ax2.set_ylabel("Quantidade")
    ax2.set_title("Distribuição por Área de Atuação")
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    st.pyplot(fig2)

    # Gráfico de Contratados vs Desistentes
    #st.subheader("📊 Contratados x Desistentes")

    # Filtra os status
    status_series = merged["situacao"].str.lower().str.strip()
    contratados = status_series.isin([
        "proposta aceita",
        "aprovado",
        "contratado pela decision",
        "contratado como hunting"
    ]).sum()

    desistentes = status_series.str.strip() == "desistiu da contratação"
    desistentes_count = desistentes.sum()

    fig3, ax3 = plt.subplots(figsize=(6, 5))
    labels = ["Contratados", "Desistentes"]
    values = [contratados, desistentes_count]
    bars = ax3.bar(labels, values, color=["green", "red"])

    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width() / 2, height + 5, f"{height}", ha='center', va='bottom', fontsize=10)

    ax3.set_ylabel("Quantidade")
    ax3.set_title("Comparativo: Contratados x Desistentes")
    st.pyplot(fig3)


elif menu == "👨‍💼 Consultores":
    st.header("👨‍💼 Consultores")
    st.markdown("""
    **Equipe de Desenvolvimento da Solução:**

    - Ozir José Azevedo Junior 
    - Paloma Cristina Pinheiro
    - Rafael Curti Barros
    - Rilciane de Sousa Bezerra

    **Instituição:** FIAP  
    **Desafio:** Datathon - IA para Recrutamento e Seleção  
    """)
