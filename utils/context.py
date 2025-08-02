import json

def buscar_contexto(pregunta):
    import os
    kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base.json')
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
        # Búsqueda simple: coincidencia parcial en la pregunta
        pregunta_lower = pregunta.lower()
        mejor_respuesta = None
        mejor_score = 0
        for item in knowledge_base:
            score = sum(1 for palabra in item['question'].lower().split() if palabra in pregunta_lower)
            if score > mejor_score:
                mejor_score = score
                mejor_respuesta = item['answer']
        if mejor_respuesta:
            return mejor_respuesta
        else:
            return "No se encontró información relevante en la base de conocimiento."
    except Exception as e:
        return f"Error al leer la base de conocimiento: {e}"
