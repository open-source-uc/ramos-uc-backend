from fastapi import FastAPI, HTTPException
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-pro')

SYSTEM_PROMPT = """Eres un moderador de contenido que evalúa comentarios. Tu tarea es determinar si un comentario es apropiado 
o inapropiado basándote en los siguientes criterios:

Criterios de moderación:
1. No debe contener lenguaje ofensivo o vulgar
2. No debe incluir amenazas o incitación a la violencia
3. No debe contener spam o contenido comercial no solicitado
4. No debe incluir información personal identificable
5. No debe contener discurso de odio o discriminación
6. Debe ser relevante al contexto académico pero tampoco muy estricto con el lenguaje

Por favor, analiza el comentario y responde únicamente con:
- "APROPIADO" si el comentario cumple con todos los criterios
- "INAPROPIADO" si viola alguno de los criterios anteriores

No incluyas explicaciones adicionales, solo responde con una de estas dos palabras."""

mensaje = "La verdad el profesor de la sección 5 de este ramo no tiene una metodología de enseñanza que me haya resultado efectiva. Sugiero revisar su método pedagógico para mejorar la experiencia de aprendizaje"

def moderar_comentario(mensaje: str):
    try:
        prompt = f"{SYSTEM_PROMPT} Comentario del usuario: {mensaje}"
        response = model.generate_content(prompt)

        if not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate response")

        if response.text.strip() == "APROPIADO":
            return True
        if response.text.strip() == "INAPROPIADO":
            return False
        
        raise HTTPException(status_code=500, detail="Unexpected response from model")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
print(moderar_comentario(mensaje))