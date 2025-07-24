import json
import pandas as pd
import re


def mapear_area(area):
    area = area.lower()
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
    elif "recursos humanos" in area or "rh" in area:
        return "RH"
    else:
        return area.title()

STATUS_POSITIVOS = [
    "proposta aceita",
    "aprovado",
    "contratado pela decision",
    "contratado como hunting",
    "desistiu da contratação"
]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def flatten_applicants(applicants):
    rows = []
    for id_, data in applicants.items():
        row = {            "applicant_id": id_,
            "nome": data["infos_basicas"].get("nome", ""),
            "email": data["infos_basicas"].get("email", ""),
            "nivel_academico": data["formacao_e_idiomas"].get("nivel_academico", ""),
            "nivel_ingles": data["formacao_e_idiomas"].get("nivel_ingles", ""),
            "nivel_espanhol": data["formacao_e_idiomas"].get("nivel_espanhol", ""),
            "area_atuacao": data["informacoes_profissionais"].get("area_atuacao", ""),
            "conhecimentos_tecnicos": data["informacoes_profissionais"].get("conhecimentos_tecnicos", ""),
            "nivel_profissional": data["informacoes_profissionais"].get("nivel_profissional", ""),
            "cv": data.get("cv_pt", "")
        }
        rows.append(row)
    return pd.DataFrame(rows)

def flatten_jobs(jobs):
    rows = []
    for id_, data in jobs.items():
        perfil = data.get("perfil_vaga", {})
        titulo_limpo = re.sub(r"[\W_]+", " ", data["informacoes_basicas"].get("titulo_vaga", "")).strip()
        row = {
            "job_id": id_,
            "titulo": titulo_limpo,
            "cliente": data["informacoes_basicas"].get("cliente", ""),
            "nivel_profissional_vaga": perfil.get("nivel profissional", ""),
            "nivel_ingles_vaga": perfil.get("nivel_ingles", ""),
            "nivel_espanhol_vaga": perfil.get("nivel_espanhol", ""),
            "area_atuacao_vaga": perfil.get("areas_atuacao", ""),
            "atividades": perfil.get("principais_atividades", ""),
            "competencias": perfil.get("competencia_tecnicas_e_comportamentais", "")
        }
        rows.append(row)
    return pd.DataFrame(rows)


def flatten_prospects(prospects):
    rows = []
    for job_id, data in prospects.items():
        for p in data["prospects"]:
            situacao = p["situacao_candidado"].strip().lower()
            foi_contratado = int(situacao in STATUS_POSITIVOS)
            rows.append({
                "job_id": job_id,
                "applicant_id": p["codigo"],
                "situacao": p["situacao_candidado"],
                "comentario": p["comentario"],
                "foi_contratado": foi_contratado
            })
    return pd.DataFrame(rows)

def merge_all(applicants_path, jobs_path, prospects_path):
    applicants = flatten_applicants(load_json(applicants_path))
    jobs = flatten_jobs(load_json(jobs_path))
    prospects = flatten_prospects(load_json(prospects_path))
    merged = prospects.merge(applicants, on="applicant_id", how="left")
    merged = merged.merge(jobs, on="job_id", how="left")
    return merged, applicants, jobs
