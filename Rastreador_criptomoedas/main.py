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

from datetime import datetime
import locale
import time
from classes import TelegramBot, CoinGeckoAPI

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

bot = TelegramBot(token='SEU TOKEN AQUI', chatID=8303989749)

# Resgatar o ID do chat do seu Bot...
#   atualizacoes = bot.get_updates()
#   print(atualizacoes[0].effective_chat.id)

api = CoinGeckoAPI(url_base='https://api.coingecko.com/api/v3')

while True:
    
    if api.ping():
        preco_brl, atualizado_em = api.get_price(coin_id='ethereum')
        
        datahora = datetime.fromtimestamp(atualizado_em).strftime('%x %X')
        
        if preco_brl < 14500:
            mensagem = f'*Cotação do Ethereum (ETH)*: \n\t*Preço*: R$ {preco_brl} \n\t*Horário*: {datahora} \n\t*Motivo*: Valor menor que o mínimo'
        elif preco_brl > 15000:
            mensagem = f'*Cotação do Ethereum (ETH)*: \n\t*Preço*: R$ {preco_brl} \n\t*Horário*: {datahora} \n\t*Motivo*: Valor maior que o máximo'
        
        if mensagem:
            bot.enviar_mensagem(mensagem=mensagem, parse_mode='MARKDOWN')
    else:
        print("API offline, tente novamente mais tarde.")
    
    # Consulta o preço a cada 5 minutos
    time.sleep(300)