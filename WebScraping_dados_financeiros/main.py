#==============================================================
# JORNADA PYTHON (Projeto 1)
# Web Scraping de dados financeiros de Fundos Imobiliários (FIIs)
#
# Uso do módulo requests para requisições HTTP e extração dos dados da tabela
# do site Fundamentus (https://fundamentus.com.br/fii_resultado.php), e com o módulo 
# BeautifulSoup faço o parsing do HTML.
#
# Após a extração, aplico uma estratégia de filtragem baseada em critérios financeiros
# e exponho os dados filtrados em uma tabela formatada com o módulo tabulate.
#==============================================================

import requests
from bs4 import BeautifulSoup
import locale
from tabulate import tabulate

from modelos import FundoImobiliario, Estrategia

# Formatação de números em pt-BR

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def trata_porcentagem(porcentagem_str):
    #25,30% -> [25,3 , None]
    return locale.atof(porcentagem_str.split("%")[0])

def trata_decimal(decimal_str):
    return locale.atof(decimal_str)

# Extração dos dados da tabela de FIIs do Fundamentus

response = requests.get("https://fundamentus.com.br/fii_resultado.php", headers={"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(response.text, "html.parser")

linhas = soup.find("table", {"id": "tabelaResultado"}).find('tbody').find_all("tr")

resultado = []

# Estabelecendo alguns critérios de filtragem

estrategia = Estrategia(
    cotacao_atual_min=50.0,
    dividend_yield_min=5,
    p_vp_min=0.7,
    valor_mercado_min=200000000,
    liquidez_min=50000,
    qt_imoveis_min=5,
    vacancia_media_max=10
)

for linha in linhas:
    dados = linha.find_all("td")
    
    codigo = dados[0].text
    segmento = dados[1].text
    cotacao_atual = trata_decimal(dados[2].text)
    ffo_yield = trata_porcentagem(dados[3].text)
    dividend_yield = trata_porcentagem(dados[4].text)
    p_vp = trata_decimal(dados[5].text)
    valor_mercado = trata_decimal(dados[6].text)
    liquidez = trata_decimal(dados[7].text)
    qt_imoveis = int(dados[8].text)
    preco_m2 = trata_decimal(dados[9].text)
    aluguel_m2 = trata_decimal(dados[10].text)
    cap_rate = trata_porcentagem(dados[11].text)
    vacancia_media = trata_porcentagem(dados[12].text)
    
    fundo = FundoImobiliario(
        codigo=codigo,
        segmento=segmento,
        cotacao_atual=cotacao_atual,
        ffo_yield=ffo_yield,
        dividend_yield=dividend_yield,
        p_vp=p_vp,
        valor_mercado=valor_mercado,
        liquidez=liquidez,
        qt_imoveis=qt_imoveis,
        preco_m2=preco_m2,
        aluguel_m2=aluguel_m2,
        cap_rate=cap_rate,
        vacancia_media=vacancia_media
    )
    
    if estrategia.aplicaEstrategia(fundo):
        resultado.append(fundo)
    

cabecalho = ["CÓDIGO", "SEGMENTO", "COTAÇÃO ATUAL", "DIVIDEND YIELD"]

tabela = []

for fundo in resultado:
    tabela.append(
        [
            fundo.codigo,
            fundo.segmento,
            f"R$ {fundo.cotacao_atual:,.2f}",
            f"{fundo.dividend_yield:.2f} %"
        ]
    )

# Geração de uma tabela com os dados filtrados

print(tabulate(tabela, headers=cabecalho, tablefmt="grid"))