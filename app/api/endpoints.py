from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from app.services.conversation_manager import process_text, get_conversation_history
from app.services.audio_processing import process_audio
from typing import Optional

router = APIRouter()

@router.post("/conversation")
async def handle_conversation(
    request: Request,
    file: UploadFile = File(None),
    text: Optional[str] = Form(None),
):
    conversation_id = request.headers.get('Conversation-ID', 'default-conversation')

    if file:
        response_audio = await process_audio(file, conversation_id)
        return FileResponse(
            response_audio, media_type="audio/wav", filename="output_audio.wav"
        )
    elif text:
        response_text = await process_text(text, conversation_id)
        if isinstance(response_text, dict) and "error" in response_text:
            return JSONResponse(content=response_text, status_code=500)
        return JSONResponse(content={"response": response_text})
    else:
        return JSONResponse(content={"error": "No valid input provided"}, status_code=400)

@router.get("/conversation/{conversation_id}")
def get_history(conversation_id: str):
    history = get_conversation_history(conversation_id)
    if isinstance(history, dict) and "error" in history:
        return JSONResponse(content=history, status_code=500)
    return {"history": history}