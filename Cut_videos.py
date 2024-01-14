import tkinter as tk
from tkinter import filedialog
import os
import cv2
import numpy
from tqdm import tqdm
from collections import deque
import subprocess
import sys
import shutil

def choisir_video():
    root = tk.Tk()
    root.withdraw()

    chemin_video = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4")])

    # Explicitly destroy the root window
    root.destroy()

    if not chemin_video:
        print("Aucune vidéo sélectionnée. Le programme s'arrête.")
        sys.exit(0)
    
    os.chdir(os.path.dirname(chemin_video))
    return chemin_video

def frame_to_time(frame_number, framerate = 30):
    seconds = frame_number / framerate
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = (seconds - int(seconds)) * 1000

    return "{:02}:{:02}:{:02}.{:03}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

def redimensionner_video(video_path):
    capture = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    largeur = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    hauteur = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    ratio = largeur / hauteur
    capture.release()

    if ratio == 9 / 16:
        return video_path
    
    print(f"Ratio de la vidéo : {ratio}")
    print(f"Largeur : {largeur}, Hauteur : {hauteur}")
    
    print("Redimensionnement de la vidéo...")
    
    nouvelle_largeur = int(hauteur * (9 / 16))

    ffmpeg_command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"crop={nouvelle_largeur}:{hauteur}",
        "original.mp4"
    ]

    # Use subprocess.Popen to capture real-time output
    process = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.returncode != 0:
        print(f"Erreur lors de l'exécution de ffmpeg : {process.stderr}")
    
    return f"{os.path.dirname(video_path)}/original.mp4"

def get_frame_rate(video_path):
    capture = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    framerate = capture.get(cv2.CAP_PROP_FPS)
    capture.release()
    return framerate

def detecter_changements_scene(video_path):
    capture = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    if not capture.isOpened():
        print(f"Erreur : Impossible d'ouvrir la vidéo à l'emplacement : {video_path}")
        return

    changements_scene = list()
    moyenne_dernieres_images = deque(maxlen=15)

    ret, frame_precedent = capture.read()
    if not ret:
        print("Erreur : Impossible de lire la première image de la vidéo.")
        capture.release()
        return

    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    with tqdm(total=total_frames, desc="Analyse vidéo", unit="frames") as pbar:
        while True:
            ret, frame_actuel = capture.read()
            if not ret:
                break

            gris_precedent = cv2.cvtColor(frame_precedent, cv2.COLOR_BGR2GRAY)
            gris_actuel = cv2.cvtColor(frame_actuel, cv2.COLOR_BGR2GRAY)

            difference = cv2.absdiff(gris_actuel, gris_precedent)
            moyenne_difference = cv2.mean(difference)[0]

            if len(moyenne_dernieres_images) < 15:
                moyenne_dernieres_images.append(moyenne_difference)
                continue

            gris = numpy.mean(moyenne_dernieres_images)
            seuil = numpy.std(moyenne_dernieres_images) * 10
            
            if abs(moyenne_difference - gris) > seuil :
                changements_scene.append(capture.get(cv2.CAP_PROP_POS_FRAMES))
                moyenne_dernieres_images.clear()

            moyenne_dernieres_images.append(moyenne_difference)

            if capture.get(cv2.CAP_PROP_POS_FRAMES) == total_frames:
                changements_scene.append(capture.get(cv2.CAP_PROP_POS_FRAMES))

            frame_precedent = frame_actuel

            pbar.update(1)

    capture.release()

    return changements_scene

def frames_finals_videos(changements_scene: list, duree_minimale: int = 10) -> list:
    dernière_coupure = 0
    for instant in changements_scene.copy()[:-1]:
        if instant - dernière_coupure < duree_minimale * framerate:
            changements_scene.remove(instant)
            continue
        dernière_coupure = instant
    return changements_scene

def decouper_et_enregistrer_videos_ffmpeg(video_path: str, changements_scene: list, duree_minimale: int = 15):
    if not shutil.which('ffmpeg'):
        print("Erreur : ffmpeg n'est pas installé sur votre système.")
        return
    
    os.makedirs('Output', exist_ok=True)

    print(f"Nombre de vidéos à découper : {len(changements_scene)}")

    finals_videos = frames_finals_videos(changements_scene, duree_minimale)
    
    dernière_coupure = 0
    with tqdm(total=len(finals_videos), desc="Découpage des vidéos") as pbar:
        for i, instant in enumerate(finals_videos):
            command = [
                "ffmpeg",
                "-i", video_path,
                "-ss", frame_to_time(dernière_coupure, framerate),
                "-to", frame_to_time(instant - 2, framerate),
                "-c:v", "libx264",
                "-c:a", "aac",
                f"Output/{i + 1}.mp4"
            ]
            dernière_coupure = instant

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(f"Erreur lors de l'exécution de ffmpeg : {result.stderr}")

            pbar.update(1)


video_a_analyser = choisir_video()
video_path = redimensionner_video(video_a_analyser)
framerate = get_frame_rate(video_path)
changements_scene = detecter_changements_scene(video_path)
# print la durée moyenne entre deux changements de scène
print(f"Durée moyenne entre deux changements de scène : {numpy.mean(numpy.diff(changements_scene)) / framerate} sec")
duree_min = int(input("Durée minimale d'une vidéo (en sec) : ")) or 15
decouper_et_enregistrer_videos_ffmpeg(video_path, changements_scene, duree_min)
