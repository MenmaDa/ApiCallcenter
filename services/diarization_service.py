from pyannote.audio import Pipeline

pipeline=Pipeline.from_pretrained(
"pyannote/speaker-diarization"
)

def separar_hablantes(
ruta_audio
):

    diarization=pipeline(
        ruta_audio
    )

    segmentos=[]

    for turno,_,speaker in diarization.itertracks(
        yield_label=True
    ):

        segmentos.append({

            "speaker":speaker,
            "inicio":round(
                turno.start,
                2
            ),

            "fin":round(
                turno.end,
                2
            )

        })

    return segmentos