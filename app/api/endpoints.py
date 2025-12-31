import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.orchestrator import orchestrator

router = APIRouter()


class GenerateDeckRequest(BaseModel):
    youtube_url: str


@router.post("/generate-deck")
async def generate_deck(request: GenerateDeckRequest):
    """
    Recebe uma URL do YouTube, processa e retorna o arquivo ZIP com os decks.
    """
    try:
        # Validação básica de URL é feita pelo Pydantic, mas podemos checar se é youtube
        if "youtube.com" not in request.youtube_url and "youtu.be" not in request.youtube_url:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        zip_path = await orchestrator.process_youtube_link(request.youtube_url)

        if not zip_path or not os.path.exists(zip_path):
            raise HTTPException(status_code=500, detail="Failed to generate deck")

        # Retorna o arquivo (FileResponse faz o stream)
        # Nota: Idealmente, deveria ser assíncrono ou usar background task para limpeza,
        # mas como FileResponse abre o arquivo, a limpeza imediata é complexa.
        # Por simplicidade neste MVP, não apagamos imediatamente após o envio nesta call.

        return FileResponse(path=zip_path, filename=os.path.basename(zip_path), media_type="application/zip")

    except Exception as e:
        # Log error properly here
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
