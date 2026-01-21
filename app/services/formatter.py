def format_transcription(json_data: dict) -> str:
    """
    Recebe o JSON do Gemini e converte em String única.
    Formato: [Inicio - Fim] Locutor: Texto
    """
    
    lines = []
    data_list = json_data.get("dados", [])
    
    for item in data_list:
        start = item["timestamp_inicio"]
        end = item["timestamp_fim"]
        speaker = item["locutor"]
        text = item["transcricao"]
        
        # Estrutura final da string:
        formatted_line = f"[{start} - {end}] {speaker}: {text}"
        lines.append(formatted_line)
    
    return "\n".join(lines)