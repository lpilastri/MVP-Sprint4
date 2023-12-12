from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base



class Fonte(Base):
    __tablename__ = 'fontes'
    
    id = Column(Integer, primary_key=True)
    name= Column("Name", String(50))
    ph = Column("pH_level", Float)
    hard = Column("Hardness", Float)
    solid = Column("Solids", Float)
    chlo = Column("Chloramines", Float)
    sulf = Column("Sulfate", Float)
    cond = Column("Conductivity", Float)
    orgcarb = Column("Organic_carbon", Float)
    trih = Column("Trihalomethanes", Float)
    turb = Column("Turbidity", Float)
    outcome = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self,name:str, ph:float, hard:float, solid:float, 
                 chlo:float, sulf:float, cond:float, 
                 orgcarb:float, trih:float, turb:float, outcome:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Fonte

        Arguments:
        name: nome do fonte
            ph: PH da água.
            hard: uma medida do conteudo mineral da água
            solid: Total de solidos dissolvidos na água
            chlo: concentração de cloramina na água
            sulf: concentração de sulfato na água
            cond: condutividade elétrica da água
            orgcarb: conteúdo de carbono orgânico na água
            trih: concentração de trihalometanos na água
            turb: turbidez da água
            outcome: diagnóstico
            data_insercao: data de quando o fonte foi inserido à base
        """
        self.name = name
        self.ph = ph
        self.hard = hard
        self.solid = solid
        self.chlo = chlo
        self.sulf = sulf
        self.cond = cond
        self.orgcarb = orgcarb
        self.trih = trih
        self.turb = turb
        self.outcome = outcome

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao