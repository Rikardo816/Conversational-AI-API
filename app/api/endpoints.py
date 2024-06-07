from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from app.core.audio_processing import process_audio, generate_audio_response
from app.core.conversation_manager import process_text, get_conversation_history
from pydantic import BaseModel
from typing import Optional
import io

router = APIRouter()


class TextRequest(BaseModel):
    text: str


# @router.post("/upload-audio/")
# async def upload_audio(file: UploadFile = File(...)):
#     if file.content_type not in ["audio/mpeg", "audio/wav", "audio/x-m4a", "audio/mp4"]:
#         raise HTTPException(status_code=400, detail="Invalid file type")

#     response_audio = await process_audio(file)

#     # Devolver el archivo de audio como una respuesta de streaming
#     # return StreamingResponse(io.BytesIO(response_audio), media_type="audio/wav")
#     return FileResponse(response_audio, media_type="audio/wav", filename="output_audio.wav")

# @router.post("/converse/")
# async def converse(input_text: str):
#     response_text = manage_conversation(input_text)
#     return {"response": response_text}

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


# @router.post("/conversation")
# async def handle_conversation(
#     request: Request,
#     file: UploadFile = File(None),
#     text: Optional[str] = Form(None),
# ):
#     conversation_id = request.headers.get('Conversation-ID', 'default-conversation')

#     if file:
#         response_audio = await process_audio(file, conversation_id)
#         return FileResponse(
#             response_audio, media_type="audio/wav", filename="output_audio.wav"
#         )
#     elif text:
#         response_text = await process_text(text, conversation_id)
#         return JSONResponse(content={"response": response_text})
#     else:
#         return JSONResponse(content={"error": "No valid input provided"}, status_code=400)



# @router.get("/conversation/{conversation_id}")
# def get_history(conversation_id: str):
#     history = get_conversation_history(conversation_id)
#     return {"history": history}
