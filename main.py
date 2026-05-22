import subprocess

from fastapi import FastAPI, UploadFile, File
import joblib
import numpy as np
import shutil
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models.models import Historial,DatasetLlamadas
from services.audio_info_service import obtener_duracion

from services.audio_service import transcribir_audio
from services.caracteristicas_service import extraer_caracteristicas
from services.predictor_service import predecir_llamada
# from services.diarization_service import separar_hablantes

Historial.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

modelo_lr=joblib.load(
    "modelo_completo1.pkl"
)

modelo_rf=joblib.load(
    "modelo_completo2.pkl"
)

modelo_gb=joblib.load(
    "modelo_completo3.pkl"
)

riesgo={

0:"Llamada normal ✅",
1:"Llamada en riesgo ⚠️",
2:"Llamada crítica 🚨"

}


@app.post("/predecir/{modelo}")
def predecir(modelo:str,data:dict):

    db=SessionLocal()

    try:

        modelos={

            "LogisticRegression":modelo_lr,
            "RandomForest":modelo_rf,
            "GradientBoosting":modelo_gb

        }

        model=modelos[modelo]

        valores=np.array([[

            data["enojo"],
            data["confusion"],
            data["tiempo"],
            data["tono"],
            data["sentimiento"],
            data["interrupciones"],
            data["tiempo_respuesta"]

        ]])

        pred=int(
            model.predict(valores)[0]
        )

        recomendaciones=[]

        if data["enojo"]>=7:

            recomendaciones.append(
                "Cliente muy enojado: hablar con tono calmado."
            )

        if data["confusion"]>=6:

            recomendaciones.append(
                "Cliente confundido: explicar mejor."
            )

        nuevo=Historial(

            modelo=modelo,
            clase=pred,
            resultado=riesgo[pred],
            recomendaciones=", ".join(
                recomendaciones
            )

        )

        db.add(nuevo)
        db.commit()

        return{

            "clase":pred,
            "resultado":riesgo[pred],
            "recomendaciones":recomendaciones

        }

    finally:

        db.close()


@app.get("/historial")
def obtener_historial():
    db = SessionLocal()
    try:
        datos = db.query(Historial).all()

        return [
            {
                "id": x.id,
                "modelo": x.modelo,
                "clase": x.clase,
                "resultado": x.resultado,
                "recomendaciones":
                    x.recomendaciones.split(", ")
                    if x.recomendaciones
                    else []
            }
            for x in datos
        ]
    finally:
        db.close()

@app.get("/historial-test")
def test():
    db = SessionLocal()
    try:
        import time
        start = time.time()

        datos = db.query(Historial).limit(5).all()

        return {
            "time": time.time() - start,
            "count": len(datos)
        }
    finally:
        db.close()

@app.post("/analizar_audio/{modelo}")
async def analizar_audio(
modelo:str,
archivo:UploadFile=File(...)
):

    db=SessionLocal()

    try:

        ruta=f"uploads/{archivo.filename}"

        with open(
            ruta,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                archivo.file,
                buffer
            )

        segmentos=[]

        texto=transcribir_audio(
            ruta
        )

        datos=extraer_caracteristicas(
            texto,
            duracion=obtener_duracion(ruta)
        )

        print(datos)

        resultado=predecir_llamada(
            modelo,
            datos
        )
        nuevoDataset=DatasetLlamadas(

            enojo=datos["enojo"],
            confusion=datos["confusion"],
            tiempo=datos["tiempo"],
            tono=datos["tono"],
            sentimiento=datos["sentimiento"],
            interrupciones=datos["interrupciones"],
            tiempo_respuesta=datos["tiempo_respuesta"],

            clase=resultado["clase"],
            resultado=resultado["resultado"]

        )

        db.add(
            nuevoDataset
        )

        # GUARDAR EN HISTORIAL
        nuevo=Historial(

            modelo=modelo,
            clase=resultado["clase"],
            resultado=resultado["resultado"],
            recomendaciones=", ".join(
                resultado["recomendaciones"]
            )

        )

        db.add(
            nuevo
        )

        db.commit()

        return{

            "transcripcion":texto,

            "hablantes":
            segmentos,

            "caracteristicas":
            datos,

            "prediccion":
            resultado

        }
    finally:

        db.close()

@app.get("/dataset")
def obtener_dataset():

    db=SessionLocal()

    try:

        datos=db.query(
            DatasetLlamadas
        ).all()

        return [

            {

            "id":x.id,
            "enojo":x.enojo,
            "confusion":x.confusion,
            "tiempo":x.tiempo,
            "tono":x.tono,
            "sentimiento":x.sentimiento,
            "interrupciones":x.interrupciones,
            "tiempo_respuesta":x.tiempo_respuesta,
            "clase":x.clase,
            "resultado":x.resultado

            }

            for x in datos
        ]

    finally:

        db.close()
        
@app.get("/test-ffmpeg")
def test_ffmpeg():
    try:
        resultado = subprocess.check_output(
            ["ffmpeg", "-version"]
        ).decode()

        return {
            "estado": "ok",
            "mensaje": resultado
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e)
        }

import os

@app.get("/debug-path")
def debug_path():
    return {
        "PATH": os.environ["PATH"],
    }