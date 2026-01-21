import os
import json
from google import genai
from dotenv import load_dotenv
from json_repair import repair_json
from google.genai.types import GenerateContentConfig, Part
from .prompt import instruction_prompt
from .schema import json_schema
from .safety_settings import filters
from .json_regex import json_extraction

load_dotenv()
PROJECT=os.environ["PROJECT_ID"]
LOCATION=os.environ["LOCATION"]
MODEL=os.environ["MODEL_GEMINI"]

try:
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)

    # Configurações do modelo
    config=GenerateContentConfig(
            temperature=0,
            audio_timestamp=True,
            response_mime_type="application/json",
            response_json_schema=json_schema,
            safety_settings=filters
            )
    
except Exception as e:
    raise RuntimeError(f"[ERRO] Falha ao inicializar cliente no Gemini: {e}")

def transcript_generation(gcs_uri: str) -> dict:
    """
    Recebe a uri de um áudio no GCS, gera a transcrição
    em formato estruturado (JSON) via Gemini e retorna os dados tratados.
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            config=config,
            contents=[
                instruction_prompt,
                Part.from_uri(
                    file_uri=gcs_uri,
                    mime_type="audio/ogg"
                ),
            ],
        )

        # Etapas de tratamento da resposta
        raw_response = json_extraction(response.text)
        treated_response = repair_json(raw_response)
        final_data = json.loads(treated_response)
        return final_data
    
    except Exception as e:
        raise RuntimeError(f"[ERRO] Falha no processamento de transcrição do Gemini: {e}")