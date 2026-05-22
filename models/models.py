from sqlalchemy import Column,Integer,String,Float
from database import Base

class Historial(Base):
    __tablename__="historial"

    id=Column(Integer,primary_key=True,index=True)

    modelo=Column(String)
    clase=Column(Integer)
    resultado=Column(String)
    recomendaciones=Column(String)

class DatasetLlamadas(Base):

    __tablename__="dataset_llamadas"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    enojo=Column(Float)
    confusion=Column(Float)
    tiempo=Column(Float)
    tono=Column(Float)
    sentimiento=Column(Float)
    interrupciones=Column(Float)
    tiempo_respuesta=Column(Float)
    clase=Column(Integer)
    resultado=Column(String)