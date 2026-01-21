import re

def json_extraction(texto):
    """
    Extrai o primeiro bloco JSON válido (Objeto ou Lista) de uma string,
    ignorando markdown e textos adicionais.
    """
    if not texto:
        raise ValueError("Resposta vazia do modelo.")
    
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", texto)
    
    if not match:
        raise ValueError(f"Nenhum JSON ({{}} ou []) encontrado na resposta:\n{texto}")

    return match.group(0)