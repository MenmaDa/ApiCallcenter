import numpy as np
import joblib

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

def predecir_llamada(
modelo,
data
):

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
        model.predict(
            valores
        )[0]
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

    if data["tono"]>=7:

        recomendaciones.append(
            "Reducir tono agresivo."
        )

    if data["interrupciones"]>=6:

        recomendaciones.append(
            "Exceso de interrupciones durante la llamada."
        )

    return{

        "clase":pred,
        "resultado":riesgo[pred],
        "recomendaciones":recomendaciones

    }