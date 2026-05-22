from textblob import TextBlob

def obtener_sentimiento(texto):

    sentimiento=TextBlob(
        texto
    ).sentiment.polarity

    return sentimiento