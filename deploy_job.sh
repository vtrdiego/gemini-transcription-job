#!/bin/bash

set -e

# Realiza a leitura do .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | sed 's/\r$//' | xargs)
else
    echo "Erro: Arquivo .env não encontrado na raiz!"
    exit 1
fi

echo "---------------------------------"
echo "Iniciando Deploy via Cloud Build"
echo "---------------------------------"

JOB_NAME="job-transcricao-audio"

gcloud run jobs deploy $JOB_NAME \
  --source . \
  --project "$PROJECT_ID" \
  --region "$LOCATION" \
  --tasks 5 \
  --task-timeout 3600s \
  --cpu 1 \
  --memory 1Gi \
  --max-retries 3 \
  --set-env-vars="PROJECT_ID=$PROJECT_ID" \
  --set-env-vars="LOCATION=$LOCATION" \
  --set-env-vars="BUCKET_NAME_GCS=$BUCKET_NAME_GCS" \
  --set-env-vars="AUDIO_FOLDER_GCS=$AUDIO_FOLDER_GCS" \
  --set-env-vars="BIGQUERY_DATASET=$BIGQUERY_DATASET" \
  --set-env-vars="BIGQUERY_TABLE=$BIGQUERY_TABLE" \
  --set-env-vars="MODEL_GEMINI=$MODEL_GEMINI"

echo "-------------------------"
echo "Deploy do Job concluído!"
echo "-------------------------"