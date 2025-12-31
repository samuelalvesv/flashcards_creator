import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.orchestrator import orchestrator

router = APIRouter()


class GenerateDeckRequest(BaseModel):
    youtube_url: str


class GenerateDeckResponse(BaseModel):
    download_url: str
    deck_count: int
    zip_filename: str


@router.post("/generate-deck", response_model=GenerateDeckResponse)
async def generate_deck(request: GenerateDeckRequest):
    """
    Recebe uma URL do YouTube, processa e retorna o link de download e a quantidade de decks.
    """
    try:
        # Validação básica de URL é feita pelo Pydantic, mas podemos checar se é youtube
        if "youtube.com" not in request.youtube_url and "youtu.be" not in request.youtube_url:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        zip_path, deck_count = await orchestrator.process_youtube_link(request.youtube_url)

        if not zip_path or not os.path.exists(zip_path):
            raise HTTPException(status_code=500, detail="Failed to generate deck")

        filename = os.path.basename(zip_path)
        # Construindo URL de download relative (assumindo host local por enquanto)
        download_url = f"/api/download/{filename}"

        return GenerateDeckResponse(download_url=download_url, deck_count=deck_count, zip_filename=filename)

    except Exception as e:
        # Log error properly here
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Endpoint para baixar o arquivo ZIP gerado.
    """
    file_path = os.path.join(orchestrator.results_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="application/zip")
