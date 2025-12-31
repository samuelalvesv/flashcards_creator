import os
from typing import Any

import httpx

from app.core.config import settings


class VideoAnkiClient:
    def __init__(self):
        self.base_url = settings.VIDEOANKI_URL
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",  # noqa: E501
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/",
            "Cookie": settings.VIDEOANKI_COOKIE_HEADER,
            "X-Csrftoken": settings.VIDEOANKI_CSRF_TOKEN,
        }

    async def upload_video(self, video_path: str, native_lang: str = "pt", target_lang: str = "en") -> str:
        """
        Envia um vídeo para processamento. Retorna o task_id.
        """
        url = f"{self.base_url}/export_deck/"

        filename = os.path.basename(video_path)

        # Dados do formulário
        data = {"target-language": target_lang, "native-language": native_lang, "order-cards-by": "chronological"}

        files = {"video-file": (filename, open(video_path, "rb"), "video/mp4")}  # noqa: SIM115 - Simple open for upload

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, data=data, files=files, timeout=60.0)
            response.raise_for_status()
            return response.json().get("task_id")

    async def check_status(self, task_id: str) -> dict[str, Any]:
        """
        Verifica o status de uma tarefa.
        """
        url = f"{self.base_url}/task_status/{task_id}"
        # O cookie pode precisar incluir o currentTaskId se o sistema depender disso,
        # mas baseado na request 2 do exemplo user, ele parece apenas retornar o status.
        # Header adicional pode ser necessário? O exemplo do usuario tem 'currentTaskId' no cookie da request 2.
        # Vamos assumir que o sistema usa o ID na URL e o cookie de sessão padrão.

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            return response.json()

    async def download_file(self, url: str) -> bytes:
        """
        Baixa o arquivo final.
        """
        async with httpx.AsyncClient() as client:
            # Pode ser necessário os mesmos headers/cookies para baixar
            response = await client.get(url, headers=self.headers, timeout=120.0)
            response.raise_for_status()
            return response.content
