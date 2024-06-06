from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from app.core.audio_processing import process_audio, generate_audio_response
from app.core.conversation_manager import manage_conversation
import io

router = APIRouter()

@router.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    if file.content_type not in ["audio/mpeg", "audio/wav", "audio/x-m4a", "audio/mp4"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    response_audio = await process_audio(file)
    
    # Devolver el archivo de audio como una respuesta de streaming
    # return StreamingResponse(io.BytesIO(response_audio), media_type="audio/wav")
    return FileResponse(response_audio, media_type="audio/wav", filename="output_audio.wav")

@router.post("/converse/")
async def converse(input_text: str):
    response_text = manage_conversation(input_text)
    return {"response": response_text}
