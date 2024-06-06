from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.audio_processing import process_audio, generate_audio_response
from app.core.conversation_manager import manage_conversation

router = APIRouter()

@router.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    if file.content_type not in ["audio/mpeg", "audio/wav"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    response_audio = await process_audio(file)
    return response_audio

@router.post("/converse/")
async def converse(input_text: str):
    response_text = manage_conversation(input_text)
    return {"response": response_text}
