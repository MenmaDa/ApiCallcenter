from services.sentimiento_service import obtener_sentimiento
import re

def extraer_caracteristicas(
    texto,
    duracion=0
):

    palabras = texto.lower()

    palabras_enojo = [
        "molesto",
        "enojado",
        "cansado",
        "terrible",
        "horrible",
        "cancelar",
        "cancelación",
        "queja",
        "mal servicio",
        "pésimo",
        "inaceptable",
        "decepcionado",
        "furioso",
        "indignado",
        "problema",
        "nunca",
        "ya estoy cansado",
        "quiero cancelar",
        "estoy harto",
        "esto es una basura",
        "malísimo"
    ]

    palabras_confusion = [
        "no entiendo",
        "qué pasó",
        "cómo",
        "por qué",
        "no sé",
        "explíqueme"
    ]

    enojo = 0
    confusion = 0

    for palabra in palabras_enojo:

        if palabra in palabras:
            enojo += 2

    for palabra in palabras_confusion:

        if palabra in palabras:
            confusion += 2


    sentimiento = obtener_sentimiento(
        texto
    )


    if sentimiento < -0.5:
        tono = 9

    elif sentimiento < -0.2:
        tono = 7

    else:
        tono = 4


    # estimación simple de interrupciones
    interrupciones = (
        texto.count("...")
        + texto.count("-")
        + texto.count("?")
    )


    return {

        "enojo":min(
            enojo,
            10
        ),

        "confusion":min(
            confusion,
            10
        ),

        # duración REAL del audio
        "tiempo":round(
            duracion,
            2
        ),

        "tono":tono,

        "sentimiento":round(
            sentimiento,
            2
        ),

        "interrupciones":min(
            interrupciones,
            10
        ),

        "tiempo_respuesta":4
    }