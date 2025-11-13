#==============================================================
# JORNADA PYTHON (Projeto 3)
# Rastreador de Criptomoedas com Notificações via Telegram
#
# Uso do módulo requests para requisições HTTP e extração do preço de uma criptomoeda
# no site coinGecko (https://api.coingecko.com), e com o módulo 
# telegram envio notificações via Bot do Telegram.
#
# Após a extração, aplico uma estratégia de filtragem baseada em critérios financeiros
# e exponho os dados filtrados em uma tabela formatada com o módulo tabulate.
#==============================================================

import requests
from datetime import datetime
import locale
import telegram
import time

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

bot = telegram.Bot(token='SEU TOKEN AQUI')

# Resgatar o ID do chat do seu Bot...
#   atualizacoes = bot.get_updates()
#   print(atualizacoes[0].effective_chat.id)

URL = 'https://api.coingecko.com/api/v3'
ENDPOINT_PING = f'{URL}/ping'
ENDPOINT_PRECO = f'{URL}/simple/price'

while True:
    resposta = requests.get(ENDPOINT_PING)
    
    if resposta.status_code == 200:
        url = f'{ENDPOINT_PRECO}?ids=ethereum&vs_currencies=BRL&include_last_updated_at=true'
        resposta = requests.get(url).json()
        
        dados_moeda = resposta.get('ethereum',None)
        preco_brl = dados_moeda.get('brl',None)
        atualizado_em = dados_moeda.get('last_updated_at',None)
        
        datahora = datetime.fromtimestamp(atualizado_em).strftime('%x %X')
        
        if preco_brl < 14500:
            mensagem = f'*Cotação do Ethereum (ETH)*: \n\t*Preço*: R$ {preco_brl} \n\t*Horário*: {datahora} \n\t*Motivo*: Valor menor que o mínimo'
        elif preco_brl > 15000:
            mensagem = f'*Cotação do Ethereum (ETH)*: \n\t*Preço*: R$ {preco_brl} \n\t*Horário*: {datahora} \n\t*Motivo*: Valor maior que o máximo'
        
        if mensagem:
            bot.send_message(chat_id=8303989749, text=mensagem, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        print("API offline, tente novamente mais tarde.")
    
    time.sleep(300)