from SoccerNet.Downloader import SoccerNetDownloader
from SoccerNet.utils import getListGames
import os
import json
import subprocess

# Parâmetros
DATASET_DIR = "./SoccerNet"
CLIPS_DIR = "./PenaltyClips"
PASSWORD = "s0cc3rn3t"
PRE_SECONDS = 5
POST_SECONDS = 5

os.makedirs(CLIPS_DIR, exist_ok=True)

# Inicializar downloader
downloader = SoccerNetDownloader(LocalDirectory=DATASET_DIR)
downloader.password = PASSWORD

# Obter todos os jogos
games = getListGames(split="train") + getListGames(split="valid") + getListGames(split="test")
ffmpeg_path = r"C:\Users\tiago1951\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
for game in games:
    label_path = os.path.join(DATASET_DIR, game, "Labels-v2.json")
    video_path = os.path.join(DATASET_DIR, game, "1_720p.mkv")

    # Descarrega etiquetas
    if not os.path.exists(label_path):
        downloader.downloadGame(game, files=["Labels-v2.json"])

    # Lê etiquetas
    if not os.path.exists(label_path):
        continue

    with open(label_path, "r") as f:
        labels = json.load(f)

    penalties = [e for e in labels["annotations"] if e["label"] == "Penalty"]

    if not penalties:
        continue

    # Descarrega o vídeo se houver penáltis
    if not os.path.exists(video_path):
        downloader.downloadGame(game, files=["1_720p.mkv"])

    # Criar clips
    for i, p in enumerate(penalties):
        timestamp = int(p["gameTime"].split(" - ")[1].split(":")[0]) * 60 + int(p["gameTime"].split(":")[1])
        clip_start = max(0, timestamp - PRE_SECONDS)
        clip_duration = PRE_SECONDS + POST_SECONDS

    

        output_file = os.path.join(CLIPS_DIR, f"{game.replace('/', '_')}_penalty_{i+1}.mp4")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        cmd = [
            ffmpeg_path,
            "-ss", str(clip_start),
            "-i", video_path,
            "-t", str(clip_duration),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-y", output_file
        ]

        print(f"🎬 A extrair penálti {i+1} de {game}...")
        subprocess.run(cmd)



