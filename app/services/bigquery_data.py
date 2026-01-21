import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()
PROJECT_ID = os.environ["PROJECT_ID"]
DATASET_ID = os.environ["BIGQUERY_DATASET"]
TABLE_ID = os.environ["BIGQUERY_TABLE"]

def insert_data(uri_audio: str, json_transcription: dict, string_transcription: str):
    """
    Insere os dados processados no BigQuery.
    Campos automáticos gerados pelo BQ:
    - id
    - data_transcricao
    """
    try:
        client = bigquery.Client(project=PROJECT_ID)
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

        # Payload de inserção dos dados
        row = {
            "uri_audio": uri_audio,
            "duracao_audio": json_transcription.get("duracao_audio_segundos", 0.0),
            "transcricao_textual": string_transcription,
            "transcricao_metadados": json.dumps(json_transcription, ensure_ascii=False)
        }
        errors = client.insert_rows_json(table_ref, [row])

        if errors:
            raise RuntimeError(f"[ERRO] Erro no Bigquery: {errors}")

    except Exception as e:
        raise RuntimeError(f"[ERRO] Falha na inserção do BigQuery: {e}")