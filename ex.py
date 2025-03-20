import csv
import json 
import os
import time
from datetime import datetime
from random import random
from sys import argv

import pandas as pd
import requests
import seaborn as sns

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

def extrair_taxa_cdi():
    try:
        response = requests.get(url=URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        return None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        return json.loads(response.text)[-1]['valor']
    
def gerar_csv():
    dado = extrair_taxa_cdi()

    if dado is None:
        print("Erro: Não foi possível obter a taxa CDI.")
        return

    for _ in range(0, 10):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

        cdi = float(dado) + (random() - 0.5)

        if not os.path.exists('./taxa-cdi.csv'):
            with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n')

        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(1)

    print("CSV gerado com sucesso.")

def gerar_grafico(nome_grafico):
    df = pd.read_csv('./taxa-cdi.csv')

    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{nome_grafico}.png")
    print(f"Gráfico salvo como {nome_grafico}.png")

def main():
    if len(argv) < 2:
        print("Por favor, forneça o nome do gráfico como parâmetro.")
        return
    
    nome_grafico = argv[1]

    gerar_csv()

    gerar_grafico(nome_grafico)

if __name__ == "__main__":
    main()