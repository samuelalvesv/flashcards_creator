import os
import subprocess
from pathlib import Path


def split_video(input_path: str, segment_time: int = 180, output_dir: str = "segments") -> list[str]:
    """
    Divide um vídeo em segmentos de 'segment_time' segundos (padrão 3 min = 180s).
    Retorna uma lista com os caminhos absolutos dos segmentos gerados.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    path_input = Path(input_path)
    # Cria diretório de output específico para este vídeo para evitar colisão
    video_output_dir = os.path.join(output_dir, path_input.stem)
    os.makedirs(video_output_dir, exist_ok=True)

    # Nome base para os segmentos: video_001.mp4, video_002.mp4, etc.
    output_pattern = os.path.join(video_output_dir, f"{path_input.stem}_%03d{path_input.suffix}")

    # Comando ffmpeg para split
    # -c copy tenta copiar o stream sem re-encode (muito mais rápido), mas pode ser impreciso no corte.
    # Como o serviço terceiro pode ser sensível, re-encoding seria mais seguro mas lento.
    # Vamos tentar re-encode para garantir compatibilidade e precisão de tempo.
    # Se ficar muito lento, podemos mudar para copy.
    # Usando -reset_timestamps 1 para cada segmento começar do 0.

    cmd = [
        "ffmpeg",
        "-i",
        input_path,
        "-c",
        "copy",  # Tentando copy primeiro pela performance
        "-map",
        "0",
        "-segment_time",
        str(segment_time),
        "-f",
        "segment",
        "-reset_timestamps",
        "1",
        output_pattern,
    ]

    # Executa o comando, suprimindo output excessivo se necessário
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    # Coleta os arquivos gerados
    generated_files = sorted(
        [
            os.path.abspath(os.path.join(video_output_dir, f))
            for f in os.listdir(video_output_dir)
            if f.startswith(path_input.stem) and f.endswith(path_input.suffix)
        ]
    )

    return generated_files
