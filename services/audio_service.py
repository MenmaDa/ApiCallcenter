import whisper
import os

modelo = whisper.load_model("base")

# ruta absoluta de ffmpeg
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

def transcribir_audio(ruta):

    resultado = modelo.transcribe(
        ruta,
        fp16=False
    )

    return resultado["text"]