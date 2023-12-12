from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
avaliador = Avaliador()

# Parâmetros    
url_dados = "https://raw.githubusercontent.com/lpilastri/MVP-Sprint4/main/water_potability.csv"
colunas = ['ph', 'hard', 'solid', 'chlo', 'sulf', 'cond', 'orgcarb', 'trih', 'turb']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados)

# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]
    
# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo_lr():  
    # Importando o modelo de regressão logística
    lr_path = 'ml_model/model_Water.pkl'
    modelo_lr = Model.carrega_modelo(lr_path)

    ml_path = 'ml_model/scaler_Water.pkl'
    scaler_ml = Model.carrega_modelo(ml_path)

    # Obtendo as métricas da Regressão Logística
    acuracia_lr, recall_lr, precisao_lr, f1_lr = avaliador.avaliar(modelo_lr, scaler_ml, X, Y)
    
    # Testando as métricas da Regressão Logística 
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_lr >= 0.75 
    assert recall_lr >= 0.5 
    assert precisao_lr >= 0.5 
    assert f1_lr >= 0.5 
 
    

