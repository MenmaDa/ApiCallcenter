from pydub import AudioSegment

def obtener_duracion(ruta):

    audio = AudioSegment.from_file(
        ruta
    )

    return audio.duration_seconds