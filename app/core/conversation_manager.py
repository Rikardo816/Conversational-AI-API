from langchain.llms import OpenAI
import os

# Obtener la API key de OpenAI desde las variables de entorno
openai_api_key = os.getenv('OPENAI_API_KEY')

conversation_cache = {}

def manage_conversation(input_text: str, session_id: str = "default"):
    if session_id not in conversation_cache:
        conversation_cache[session_id] = []
    conversation_cache[session_id].append({"user": input_text})
    
    llm = OpenAI(api_key=openai_api_key)
    response = llm.generate([input_text])  # Pasar una lista de cadenas
    response_text = response.generations[0][0].text  # Acceder al texto de la respuesta
    conversation_cache[session_id].append({"bot": response_text})
    
    return response_text
