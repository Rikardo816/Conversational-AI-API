from app.services.conversation_history import save_message, get_messages
from langchain.llms import OpenAI
import os

openai_api_key = os.getenv('OPENAI_API_KEY')


async def process_text(user_text, conversation_id):
    # Procesar la respuesta
    response_text = f"Processed: {user_text}"
    

    llm = OpenAI(api_key=openai_api_key)
    response = llm.generate([user_text])  # Pasar una lista de cadenas
    response_text = response.generations[0][0].text  # Acceder al texto de la respuesta

    # Guardar en el historial
    # save_message(conversation_id, user_text)
    # save_message(conversation_id, response_text)
    
    return response_text

def get_conversation_history(conversation_id):
    return get_messages(conversation_id)



# # Obtener la API key de OpenAI desde las variables de entorno
# openai_api_key = os.getenv('OPENAI_API_KEY')

# conversation_cache = {}

# def manage_conversation(input_text: str, session_id: str = "default"):
#     if session_id not in conversation_cache:
#         conversation_cache[session_id] = []
#     conversation_cache[session_id].append({"user": input_text})
    
#     llm = OpenAI(api_key=openai_api_key)
#     response = llm.generate([input_text])  # Pasar una lista de cadenas
#     response_text = response.generations[0][0].text  # Acceder al texto de la respuesta
#     conversation_cache[session_id].append({"bot": response_text})
    
#     return response_text
