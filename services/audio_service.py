import whisper

modelo = whisper.load_model("base")

def transcribir_audio(ruta):

    resultado = modelo.transcribe(
        ruta,
        fp16=False
    )

    return resultado["text"]