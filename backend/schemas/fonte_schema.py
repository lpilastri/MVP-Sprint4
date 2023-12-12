from pydantic import BaseModel
from typing import Optional, List
from model.fonte import Fonte
import json
import numpy as np

class FonteSchema(BaseModel):
    """ Define como um novo fonte a ser inserido deve ser representado
    """
    name: str = "Aguas Claras"
    ph: float = 6
    hard: float = 148
    solid: float = 72
    chlo: float = 35
    sulf: float = 2
    cond: float = 33.6
    orgcarb: float = 0.627
    trih: float = 50
    turb: int = 50
    
class FonteViewSchema(BaseModel):
    """Define como um fonte será retornado
    """
    id: int = 1
    name: str = "Aguas Claras"
    ph: float = 6
    hard: float = 148
    solid: float = 72
    chlo: float = 35
    sulf: float = 0
    cond: float = 33.6
    orgcarb: float = 0.627
    trih: float = 50
    turb: float = 50
    outcome: int = None
    
class FonteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do fonte.
    """
    name: str = "Aguas Claras"

class ListaFonteschema(BaseModel):
    """Define como uma lista de fontes será representada
    """
    fontes: List[FonteSchema]

    
class FonteDelSchema(BaseModel):
    """Define como um fonte para deleção será representado
    """
    name: str = "Aguas Claras"
    
# Apresenta apenas os dados de um fonte    
def apresenta_fonte(fonte: Fonte):
    """ Retorna uma representação do fonte seguindo o schema definido em
        FonteViewSchema.
    """
    return {
        "id": fonte.id,
        "name": fonte.name,
        "ph": fonte.ph,
        "hard": fonte.hard,
        "solid": fonte.solid,
        "chlo": fonte.chlo,
        "sulf": fonte.sulf,
        "cond": fonte.cond,
        "orgcarb": fonte.orgcarb,
        "trih": fonte.trih,
        "turb": fonte.turb,
        "outcome": fonte.outcome
    }
    
# Apresenta uma lista de fontes
def apresenta_fontes(fontes: List[Fonte]):
    """ Retorna uma representação do fonte seguindo o schema definido em
        FonteViewSchema.
    """
    result = []
    for fonte in fontes:
        result.append({
            "id": fonte.id,
            "name": fonte.name,
            "ph": fonte.ph,
            "hard": fonte.hard,
            "solid": fonte.solid,    
            "chlo": fonte.chlo,
            "sulf": fonte.sulf,
            "cond": fonte.cond,
            "orgcarb": fonte.orgcarb,
            "trih": fonte.trih,
            "turb": fonte.turb,
            "outcome": fonte.outcome
        })

    return {"fontes": result}

