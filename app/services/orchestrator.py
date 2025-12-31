import asyncio
import os
import zipfile

from app.services.anki import VideoAnkiClient
from app.services.video import split_video
from app.services.youtube import download_youtube_video


class ProcessingOrchestrator:
    def __init__(self):
        self.anki_client = VideoAnkiClient()
        self.download_dir = "temp_downloads"
        self.segments_dir = "temp_segments"
        self.results_dir = "temp_results"

        for d in [self.download_dir, self.segments_dir, self.results_dir]:
            os.makedirs(d, exist_ok=True)

    async def process_youtube_link(self, youtube_url: str) -> tuple[str, int]:
        """
        Executa o fluxo completo e retorna o caminho do arquivo ZIP final e a quantidade de decks.
        """
        # 1. Download do YouTube
        print(f"Baixando vídeo: {youtube_url}")
        video_path = await asyncio.to_thread(download_youtube_video, youtube_url, self.download_dir)

        # 2. Split do Video
        print(f"Dividindo vídeo: {video_path}")
        segments = await asyncio.to_thread(split_video, video_path, 180, self.segments_dir)

        # 3. Processar cada segmento
        tasks = []
        for segment in segments:
            tasks.append(self._process_segment(segment))

        # Executa em paralelo (com limite se necessário, mas o serviço parece aguentar poucos concorrentes)
        # Para evitar sobrecarga no servidor terceiro, vamos usar um semáforo se for muitos videos.
        # Por enquanto, gather direto.
        apkg_files = await asyncio.gather(*tasks)

        # 4. Criar ZIP
        final_zip_path = os.path.join(self.results_dir, f"deck_{os.path.basename(video_path)}.zip")
        with zipfile.ZipFile(final_zip_path, "w") as zipf:
            for apkg in apkg_files:
                if apkg and os.path.exists(apkg):
                    zipf.write(apkg, os.path.basename(apkg))

        # Limpeza (opcional, pode ser movido para background task depois)
        # shutil.rmtree(self.download_dir)
        # Manter arquivos temporários por enquanto para debug

        deck_count = len(apkg_files)
        return final_zip_path, deck_count

    async def _process_segment(self, video_path: str) -> str:
        """
        Envia um segmento, espera ficar pronto e baixa o resultado.
        """
        try:
            print(f"Enviando segmento: {os.path.basename(video_path)}")
            task_id = await self.anki_client.upload_video(video_path)

            # Polling
            while True:
                await asyncio.sleep(2)  # Espera 2s entre checagens conforme solicitado
                status_data = await self.anki_client.check_status(task_id)
                status = status_data.get("status")

                if status == "SUCCESS":
                    download_url = status_data.get("result", {}).get("download_url")
                    apkg_filename = status_data.get("result", {}).get("apkg_filename", "deck.apkg")

                    if not download_url:
                        raise Exception("Download URL not found in success response")

                    # Download APKG
                    print(f"Segmento pronto, baixando: {apkg_filename}")
                    content = await self.anki_client.download_file(download_url)
                    output_path = os.path.join(self.results_dir, apkg_filename)
                    with open(output_path, "wb") as f:
                        f.write(content)
                    return output_path

                elif status == "RUNNING":
                    progress = status_data.get("progress", 0)
                    step = status_data.get("current_task", "processing")
                    print(f"Task {task_id}: {status} - {step} ({progress}%)")
                    continue

                elif status == "FAILURE" or status == "ERROR":
                    print(f"Falha no processamento do segmento {video_path}: {status_data}")
                    raise Exception(f"Task failed: {status}")

                # Outros status (PENDING, etc)
                print(f"Task {task_id} status: {status}")

        except Exception as e:
            print(f"Erro ao processar segmento {video_path}: {e}")
            return ""  # Retorna vazio ou trata como erro


orchestrator = ProcessingOrchestrator()
