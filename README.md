# Projet de Découpage Vidéo et Génération de Descriptions

Ce projet consiste en deux scripts Python permettant de découper des vidéos en segments en utilisant des changements de scène détectés et de générer des descriptions multilignes pour ces segments. Les scripts utilisent les bibliothèques Python `tkinter`, `cv2` (OpenCV), `numpy`, `tqdm`, `subprocess`, `sys`, `shutil`, `time`, et `keyboard`.

## Script 1: `Cut_videos.py`

Ce script propose les fonctionnalités suivantes :

- **choisir_video() :** Ouvre une boîte de dialogue pour sélectionner un fichier vidéo au format mp4.
- **frame_to_time(frame_number, framerate):** Convertit le numéro de trame en format de temps (HH:MM:SS.MMM).
- **redimensionner_video(video_path):** Redimensionne la vidéo en 16:9 si nécessaire en utilisant `ffmpeg`.
- **get_frame_rate(video_path):** Récupère le taux de trame de la vidéo.
- **detecter_changements_scene(video_path):** Détecte les changements de scène dans la vidéo.
- **frames_finals_videos(changements_scene, duree_minimale):** Filtre les instants de changement de scène en fonction d'une durée minimale.
- **decouper_et_enregistrer_videos_ffmpeg(video_path, changements_scene, duree_minimale):** Utilise `ffmpeg` pour découper et enregistrer les vidéos.

**Utilisation :** Exécutez le script en choisissant une vidéo à découper.

## Script 2: `Write_text.py`

Ce script propose les fonctionnalités suivantes :

- **get_multiline_text():** Ouvre une fenêtre tkinter pour que l'utilisateur entre des descriptions multilignes.
- **write(description):** Écrit le texte passé en paramètre avec le clavier, simulant des frappes avec des délais.

**Utilisation :** Exécutez le script, entrez les descriptions dans la fenêtre qui s'ouvre, puis appuyez sur Entrée pour commencer.

## Instructions pour exécuter les scripts :

1. Assurez-vous d'avoir Python installé sur votre système.
2. Installez les dépendances nécessaires en utilisant `pip install -r requirements.txt` (si un fichier `requirements.txt` est fourni).
3. Exécutez les scripts selon les instructions d'utilisation mentionnées ci-dessus.

N'hésitez pas à contribuer, à signaler des problèmes ou à suggérer des améliorations !
