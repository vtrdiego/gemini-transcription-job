json_schema={
        "type": "object",
        "properties": {
            "duracao_audio_segundos": {"type": "number"},
            "dados": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "locutor": {"type": "string"},
                        "timestamp_inicio": {"type": "number"},
                        "timestamp_fim": {"type": "number"},
                        "transcricao": {"type": "string"}
                    },
                    "required": [
                        "locutor",
                        "timestamp_inicio",
                        "timestamp_fim",
                        "transcricao"
                    ]
                }
            }
        },
        "required": ["duracao_audio_segundos", "dados"]
    }