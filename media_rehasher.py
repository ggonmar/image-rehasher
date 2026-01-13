import os
import subprocess
import random
from datetime import timedelta
from PIL import Image

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def copy_all_metadata(src, dst):
    subprocess.run([
        "exiftool",
        "-TagsFromFile", src,
        "-all:all",
        "-unsafe",
        "-icc_profile",
        "-overwrite_original",
        dst
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def shift_dates(dst, delta_ms):
    # convertir delta a segundos con milisegundos
    delta_seconds = delta_ms / 1000.0
    delta_str = f"0:0:0 0:0:{delta_seconds:.3f}"
    subprocess.run([
        "exiftool",
        f"-AllDates+={delta_str}",
        "-overwrite_original",
        dst
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_image(file_path, out_path):
    with Image.open(file_path) as img:
        # Escalado 0.1% y crop para volver a tamaño original
        new_size = (int(img.width * 1.001), int(img.height * 1.001))
        resized = img.resize(new_size, Image.LANCZOS)

        left = (resized.width - img.width) // 2
        top = (resized.height - img.height) // 2
        right = left + img.width
        bottom = top + img.height

        cropped = resized.crop((left, top, right, bottom))
        cropped.save(out_path, quality=100,  optimize=True)

    # Copiar EXIF completo
    subprocess.run([
        "exiftool",
        "-TagsFromFile", file_path,
        "-all:all",
        "-overwrite_original",
        out_path
    ])

    copy_all_metadata(file_path, out_path)
    delta_ms = random.randint(100, 200)
    shift_dates(out_path, delta_ms)

def process_video(file_path, out_path):
    # Reencode suave
    subprocess.run([
        "ffmpeg", "-y",
        "-i", file_path,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "copy",
        out_path
    ])

    # Copiar metadatos
    subprocess.run([
        "exiftool",
        "-TagsFromFile", file_path,
        "-all:all",
        "-overwrite_original",
        out_path
    ])

    # Ajustar fechas con delta
    delta_ms = random.randint(100, 200)
    shift_dates(out_path, delta_ms)

def main():
    for root, _, files in os.walk(INPUT_DIR):
        for f in files:
            in_path = os.path.join(root, f)
            name, ext = os.path.splitext(f)
            out_path = os.path.join(OUTPUT_DIR, name + "_new" + ext.lower())

            ext = ext.lower()
            if ext in [".jpg", ".jpeg", ".png", ".heic"]:
                print(f"Procesando imagen: {f}")
                process_image(in_path, out_path)
            elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
                print(f"Procesando vídeo: {f}")
                process_video(in_path, out_path)
            else:
                print(f"Saltando {f}, extensión no soportada.")

if __name__ == "__main__":
    main()