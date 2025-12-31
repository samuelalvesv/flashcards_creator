from fastapi import FastAPI

from app.api.endpoints import router as api_router

app = FastAPI(
    title="Flashcards Creator API",
    description="API para criar decks Anki a partir de vídeos do YouTube",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Flashcards Creator API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
