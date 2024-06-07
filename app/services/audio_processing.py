import io
import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from fastapi import UploadFile
from gtts import gTTS
from langchain_openai import OpenAI
# from app.services.conversation_history import save_message

# Configurar logging
logger = logging.getLogger(__name__)

# Cargar las variables de entorno desde el archivo .env
from dotenv import load_dotenv
load_dotenv()

# Obtener la API key de OpenAI desde las variables de entorno
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables")

# Convertir el archivo de audio a texto
def audio_to_text(audio_data: bytes):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(io.BytesIO(audio_data))
    with audio_file as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        return text
    except sr.UnknownValueError:
        logger.error("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Convertir el archivo de audio a formato WAV
def convert_to_wav(file: UploadFile):
    audio = AudioSegment.from_file(file.file, format=file.filename.split('.')[-1])
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io.read()

# Convertir texto a audio
def text_to_audio(text: str, format: str = "wav"):
    logger.debug(f"Converting text to audio: {text}")
    # Utilizar gTTS para convertir texto a audio y trabajar en memoria
    tts = gTTS(text=text, lang='es')
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    logger.debug(f"Generated MP3 Audio File Length: {len(audio_io.getvalue())} bytes")
    
    # Convertir el audio a WAV si es necesario
    if format != "mp3":
        audio = AudioSegment.from_file(audio_io, format="mp3")
        wav_io = io.BytesIO()
        audio.export(wav_io, format=format)
        wav_io.seek(0)
        logger.debug(f"Generated WAV Audio File Length: {len(wav_io.getvalue())} bytes")
        return wav_io.getvalue()
    
    return audio_io.getvalue()

# Procesar el audio y generar una respuesta
async def process_audio(file, conversation_id):
    # Convertir el archivo de audio a texto
    wav_data = convert_to_wav(file)
    text = audio_to_text(wav_data)
    logger.debug(f"Transcribed Text: {text}")
    if not text:
        return text_to_audio("Could not transcribe the audio", format="wav")
    
    # save_message(conversation_id, "user", text)

    # Especificar el modelo al inicializar OpenAI
    llm = OpenAI(api_key=openai_api_key)
    
    # Ajustar el prompt para pedir respuestas más cortas
    prompt = f"Responde brevemente: {text}"
    
    # Ajustar los parámetros del modelo
    response = llm.generate(
        prompts=[prompt],
        max_tokens=50,  # Limitar la longitud de la respuesta
        temperature=0.5,  # Controlar la creatividad de la respuesta
        top_p=0.9  # Usar nucleus sampling para obtener respuestas más enfocadas
    )

     # Registro completo de la respuesta
    logger.debug(f"OpenAI Response: {response}")

    if response.generations and response.generations[0]:
        response_text = response.generations[0][0].text
    else:
        response_text = "No response from the model."

    # save_message(conversation_id, "system", response_text)
    logger.debug(f"Generated Response Text: {response_text}")
    audio_file = text_to_audio(response_text, format="wav")
    logger.debug(f"Generated Audio File Length: {len(audio_file)} bytes")

    # Guardar el archivo de audio temporalmente
    audio_path = "/tmp/output_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_file)

    return audio_path  # Devolver la ruta del archivo en lugar de FileResponse

def generate_audio_response(text: str):
    return text_to_audio(text)
