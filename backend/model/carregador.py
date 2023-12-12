import pandas as pd

class Carregador:

    def carregar_dados(self, url: str):
        """ Carrega e retorna um DataFrame. Há diversos parâmetros 
        no read_csv que poderiam ser utilizados para dar opções 
        adicionais.
        """
        #tratamento dados
        df = pd.read_csv(url)

        target = 'Potability'
        labels = [0, 1]
        features = [i for i in df.columns.values if i not in [target]]

        df['ph'].fillna(df['ph'].mean(),axis=0, inplace=True)   
        df['Sulfate'].fillna(df['Sulfate'].mean(),axis=0, inplace=True)
        df['Trihalomethanes'].fillna(df['Trihalomethanes'].mean(),axis=0, inplace=True)
        return df # Esses dois parâmetros são próprios para uso deste dataset. Talvez você não precise utilizar
    