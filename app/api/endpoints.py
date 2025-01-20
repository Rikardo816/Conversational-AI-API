from fastapi import APIRouter, Request, File, UploadFile, Form, WebSocket
from fastapi.responses import JSONResponse, FileResponse

from app.services.conntection_manager import ConnectionManager
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


manager = ConnectionManager()

import logging
from datetime import datetime

# Configurar el logger
logger = logging.getLogger("websocket_endpoint")
logger.setLevel(logging.DEBUG)

# Crear un handler para la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Crear un formato personalizado
formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Agregar el handler al logger
logger.addHandler(console_handler)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"New connection established - Client: {client_id} - Session: {session_id}")

    await manager.connect(websocket)
    try:
        while True:
            logger.debug(f"[{session_id}] Waiting for message from client {client_id}")
            text = await websocket.receive_text()
            logger.info(f"[{session_id}] Received message from {client_id}: {text}")

            try:
                logger.debug(f"[{session_id}] Processing text for {client_id}")
                response = await process_text(text, client_id)
                logger.debug(f"[{session_id}] Response generated for {client_id}: {response}")

                message = response["content"] if "content" in response else response["response"]["content"]
                logger.info(f"[{session_id}] Sending response to {client_id}: {message}")

                await manager.send_message(message, websocket)
                logger.info(f"[{session_id}] Response sent successfully to {client_id}")

            except Exception as e:
                logger.error(f"[{session_id}] Error processing message for {client_id}: {str(e)}",
                             exc_info=True)

    except Exception as e:
        logger.error(f"[{session_id}] WebSocket error for {client_id}: {str(e)}",
                     exc_info=True)
        await manager.disconnect(websocket)
    finally:
        logger.info(f"[{session_id}] Connection closed for client {client_id}")
