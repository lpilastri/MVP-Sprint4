from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Fonte, Model
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
fonte_tag = Tag(name="Fonte", description="Adição, visualização, remoção e predição de fontes")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de fontes
@app.get('/fontes', tags=[fonte_tag],
         responses={"200": FonteViewSchema, "404": ErrorSchema})
def get_fontes():
    """Lista todos os fontes cadastrados na base
    Retorna uma lista de fontes cadastrados na base.
    
    Args:
        nome (str): nome do fonte
        
    Returns:
        list: lista de fontes cadastrados na base
    """
    session = Session()
    
    # Buscando todos os fontes
    fontes = session.query(Fonte).all()
    
    if not fontes:
        logger.warning("Não há fontes cadastrados na base :/")
        return {"message": "Não há fontes cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d fontes econtrados" % len(fontes))
        return apresenta_fontes(fontes), 200


# Rota de adição de fonte
@app.post('/fonte', tags=[fonte_tag],
          responses={"200": FonteViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: FonteSchema):
    """Adiciona um novo fonte à base de dados
    Retorna uma representação das fontes e diagnósticos associados.
    
    Args:
        name (str): nome do fonte
        ph (int): número de vezes que engravidou: Pregnancies
        hard (int): concentração de glicose no plasma: Glucose
        solid (int): pressão diastólica (mm Hg): BloodPressure
        chlo (int): espessura da dobra cutânea do tríceps (mm): SkinThickness
        sulf (int): insulina sérica de 2 horas (mu U/ml): Insulin
        cond (float): índice de massa corporal (peso em kg/(altura em m)^2): BMI
        orgcarb (float): função pedigree de diabetes: DiabetesPedigreeFunction
        trih (int): idade (anos): Age
        turb (float):
        
    Returns:
        dict: representação do fonte e diagnóstico associado
    """
    
    # Carregando modelo
    ml_path = 'ml_model/model_Water.pkl'
    modelo = Model.carrega_modelo(ml_path)
    
    fonte = Fonte(
        name=form.name.strip(),
        ph=form.ph,
        hard=form.hard,
        solid=form.solid,
        chlo=form.chlo,
        sulf=form.sulf,
        cond=form.cond,
        orgcarb=form.orgcarb,
        trih=form.trih,
        turb=form.turb,
        outcome=Model.preditor(modelo, form)
    )
    logger.debug(f"Adicionando produto de nome: '{fonte.name}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se fonte já existe na base
        if session.query(Fonte).filter(Fonte.name == form.name).first():
            error_msg = "Fonte já existente na base :/"
            logger.warning(f"Erro ao adicionar fonte '{fonte.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando fonte
        session.add(fonte)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado fonte de nome: '{fonte.name}'")
        return apresenta_fonte(fonte), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar fonte '{fonte.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de fonte por nome
@app.get('/fonte', tags=[fonte_tag],
         responses={"200": FonteViewSchema, "404": ErrorSchema})
def get_fonte(query: FonteBuscaSchema):    
    """Faz a busca por um fonte cadastrado na base a partir do nome

    Args:
        nome (str): nome do fonte
        
    Returns:
        dict: representação do fonte e diagnóstico associado
    """
    
    fonte_nome = query.name
    logger.debug(f"Coletando dados sobre produto #{fonte_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    fonte = session.query(Fonte).filter(Fonte.name == fonte_nome).first()
    
    if not fonte:
        # se o fonte não foi encontrado
        error_msg = f"Fonte {fonte_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{fonte_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Fonte econtrado: '{fonte.name}'")
        # retorna a representação do fonte
        return apresenta_fonte(fonte), 200
   
    
# Rota de remoção de fonte por nome
@app.delete('/fonte', tags=[fonte_tag],
            responses={"200": FonteViewSchema, "404": ErrorSchema})
def delete_fonte(query: FonteBuscaSchema):
    """Remove um fonte cadastrado na base a partir do nome

    Args:
        nome (str): nome do fonte
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    fonte_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre fonte #{fonte_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando fonte
    fonte = session.query(Fonte).filter(Fonte.name == fonte_nome).first()
    
    if not fonte:
        error_msg = "Fonte não encontrado na base :/"
        logger.warning(f"Erro ao deletar fonte '{fonte_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(fonte)
        session.commit()
        logger.debug(f"Deletado Fonte #{fonte_nome}")
        return {"message": f"Fonte {fonte_nome} removido com sucesso!"}, 200