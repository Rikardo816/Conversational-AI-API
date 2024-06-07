from typing import Optional
import os
import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from redis import Redis
from langchain_community.chat_message_histories import RedisChatMessageHistory
from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse

router = APIRouter()

# Configurar la API Key de OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

# Conectar a Redis
try:
    redis_client = Redis(host='redis', port=6379, db=0)
    redis_client.ping()
    logging.info("Connected to Redis successfully.")
except Exception as e:
    logging.error(f"Could not connect to Redis: {e}")
    raise ConnectionError("Could not connect to Redis. Ensure Redis is running.") from e

# Definir el prompt de la conversación
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# Crear una instancia del modelo de lenguaje
llm = ChatOpenAI(api_key=openai_api_key)

# Crear la cadena de procesamiento con el historial de mensajes
chain = prompt | llm
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: RedisChatMessageHistory(
        session_id, url="redis://redis:6379"
    ),
    input_messages_key="question",
    history_messages_key="history",
)

def make_serializable(obj):
    """
    Convert non-serializable objects to a serializable format.
    """
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(i) for i in obj]
    elif hasattr(obj, '__dict__'):
        return {k: make_serializable(v) for k, v in obj.__dict__.items()}
    else:
        return obj

async def process_text(user_text, conversation_id):
    try:
        # Configurar la cadena con el ID de la conversación
        config = {"configurable": {"session_id": conversation_id}}
        
        # Procesar la respuesta
        response = chain_with_history.invoke({"question": user_text}, config=config)
        
        # Asegurarse de que la respuesta sea serializable
        serializable_response = make_serializable(response)
        
        return serializable_response
    except Exception as e:
        # Manejar errores y retornar un mensaje de error
        logging.error(f"Error processing text: {e}")
        return {"error": str(e)}

def get_conversation_history(conversation_id):
    try:
        # Recuperar el historial de la conversación desde Redis
        history = RedisChatMessageHistory(conversation_id, redis_client)
        messages = history.get_messages()
        
        # Convertir los mensajes al formato deseado
        formatted_messages = [msg['content'] for msg in messages]
        
        return formatted_messages
    except Exception as e:
        # Manejar errores y retornar un historial vacío
        logging.error(f"Error retrieving conversation history: {e}")
        return {"error": str(e)}
