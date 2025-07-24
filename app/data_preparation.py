
import os
import json
import pandas as pd

def load_applicants_from_parts(base_path="data"):
    parts = ["applicants_part_1.json", "applicants_part_2.json", "applicants_part_3.json"]
    all_data = {}
    for part in parts:
        with open(os.path.join(base_path, part), "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.update(data)
    df = pd.DataFrame.from_dict(all_data, orient="index").reset_index()
    df = df.rename(columns={"index": "applicant_id"})
    return df


# --- CÓDIGO ORIGINAL ---

import json
import pandas as pd
import re
import os

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

def load_multiple_jsons(paths):
    combined = {}
    for path in paths:
        if os.path.exists(path):
            data = load_json(path)
            combined.update(data)
    return combined

def flatten_applicants(applicants):
    rows = []
    for id_, data in applicants.items():
        row = {
            "applicant_id": id_,
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

def merge_all(applicants_paths, jobs_path, prospects_path):
    applicants_raw = load_applicants_from_parts(base_path="data")
    applicants = flatten_applicants(applicants_raw.to_dict(orient="index"))

    jobs = flatten_jobs(load_json(jobs_path))
    prospects = flatten_prospects(load_json(prospects_path))
    
    applicants["applicant_id"] = applicants["applicant_id"].astype(str)
    prospects["applicant_id"] = prospects["applicant_id"].astype(str)

    merged = prospects.merge(applicants, on="applicant_id", how="left")
    merged = merged.merge(jobs, on="job_id", how="left")
    return merged, applicants, jobs
