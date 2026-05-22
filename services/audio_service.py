import os
import shutil
import subprocess
import whisper

modelo = whisper.load_model("base")


def configurar_ffmpeg():
    ffmpeg_path = shutil.which("ffmpeg")

    if not ffmpeg_path:
        print("⚠️ FFmpeg no encontrado")
        return

    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)


def transcribir_audio(ruta):
    configurar_ffmpeg()

    try:
        subprocess.check_output(["ffmpeg", "-version"])
    except Exception as e:
        print("ERROR FFMPEG:", e)

    resultado = modelo.transcribe(ruta, fp16=False)
    return resultado["text"]