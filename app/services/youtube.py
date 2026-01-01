import os

import yt_dlp


def download_youtube_video(url: str, output_dir: str = "downloads") -> str:
    """
    Baixa um vídeo do YouTube.
    Retorna o caminho absoluto do arquivo baixado.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Configurações do yt-dlp
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "overwrites": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.abspath(filename)
