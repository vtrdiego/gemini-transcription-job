import os
from dotenv import load_dotenv
from google.cloud import storage
from llm.gemini import transcript_generation
from services.formatter import format_transcription
from services.bigquery_data import insert_data

load_dotenv()

# Configurações
BUCKET_NAME = os.environ["BUCKET_NAME_GCS"]
AUDIO_FOLDER = os.environ["AUDIO_FOLDER_GCS"]
TASK_INDEX = int(os.environ.get("CLOUD_RUN_TASK_INDEX", 0))
TASK_COUNT = int(os.environ.get("CLOUD_RUN_TASK_COUNT", 1))

def main_orchestration():
    """
    Orquestra a execução da pipeline:
    - Lista os áudios no bucket
    - Distribui o processamento entre as tasks
    - Executa a pipeline de transcrição e persistência
    """

    try:
        client = storage.Client()
        
        blobs = list(client.list_blobs(BUCKET_NAME, prefix=AUDIO_FOLDER))
        blobs.sort(key=lambda x: x.name)
        
        for i, blob in enumerate(blobs):
            
            if blob.name.endswith('/'):
                continue

            # Distribui os audios entre as tasks por índice fixo
            if i % TASK_COUNT == TASK_INDEX:
                
                # Fluxo de processamento do áudio:
                uri_audio=f"gs://{BUCKET_NAME}/{blob.name}"
                json_transcription = transcript_generation(uri_audio)
                string_transcription = format_transcription(json_transcription)
                insert_data(uri_audio, json_transcription, string_transcription)

    except Exception as e:
        raise RuntimeError(f"[ERRO] Falha na execução do main: {e}")

if __name__ == "__main__":
    main_orchestration()