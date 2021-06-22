# ================================================ #
#                   Bibliotecas                    #
# ================================================ #

import json
import folium
import pandas as pd
from collections import Counter
import copy

# ================================================ #
#                       Base                       #
# ================================================ #

# Caminho e nome do arquivo
path = "datasets"

# Base de dados, [6958 rows x 4 columns]. Colunas: Entity, Code, Year, Number of people without access to electricity
db_pessoas_sem_eletricidade = pd.read_csv(f"{path}/people-without-electricity-country.csv")

# GeoJson de países
db_paises = json.load(open(f"{path}/countries.geojson"))

# ================================================ #
#                     Código                       #
# ================================================ #

def frequencia(lista):
    """Conta a frequência dos elementos de 'lista' e retorna uma lista de tuplas com elas"""
    
    tabela = Counter(lista)
    freq_numeros = tabela.most_common()
    return freq_numeros

# Para cada ano único na base de dados, itera uma vez
for ano in frequencia(db_pessoas_sem_eletricidade["Year"]):
    
    # Cria o mapa de fundo
    map = folium.Map(location=[-0.001545, 51.477928], zoom_start=2)

    # Cria uma deepcopy da base original para não alterar acidentalmente os arquivos nela
    db_pessoas_sem_eletricidade_por_ano = copy.deepcopy(db_pessoas_sem_eletricidade)

    # Separa a base de dados por linha, checa se a linha tem o ano sendo considerado e se não tiver, exclui a linha    
    for linha in range(len(db_pessoas_sem_eletricidade_por_ano)):
        if db_pessoas_sem_eletricidade_por_ano['Year'][linha] != ano[0]:
            db_pessoas_sem_eletricidade_por_ano = db_pessoas_sem_eletricidade_por_ano.drop(linha)

    # Cria uma camada Choropleth com os dados
    folium.Choropleth(
        geo_data=db_paises,
        name='choropleth',
        data=db_pessoas_sem_eletricidade_por_ano,
        columns=['Entity', 'Number of people without access to electricity'],
        key_on='feature.properties.ADMIN',
        fill_opacity=0.7,
        fill_color='YlGn',
        line_opacity=0.2,
        nan_fill_color='#ffffff',
        # Todos que são 0 ou NaN estão como branco
        bins=[0, 12500000, 25000000, 50000000, 75000000, 100000000, 200000000, 6000000000],  
        # Como o bins requer que o último número seja maior que todos os dados, não mostra direito a linha de mudança de cores 
        legend_name=f'Número de pessoas sem acesso a eletricidade por país em {ano[0]}
    ).add_to(map)
    
    # Salva o mapa antes de iterar novamente
    map.save(f"{path}/Número de pessoas sem acesso a eletricidade por país em {ano[0]}.html")
