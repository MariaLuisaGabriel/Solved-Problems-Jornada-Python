import requests
import telegram

class CoinGeckoAPI:
    def __init__(self, url_base: str):
        self.url_base = url_base
    
    def ping(self) -> bool:
        print("Verificando se a API está online...")
        
        ENDPOINT_PING = f'{self.url_base}/ping'
        resposta = requests.get(ENDPOINT_PING)
        
        return resposta.status_code == 200

    def get_price(self, coin_id: str, vs_currency: str = 'brl') -> dict:
        print(f"Consultando preço da criptomoeda {coin_id} em {vs_currency}...")
        
        url = f'{self.url_base}/simple/price?ids={coin_id}&vs_currencies={vs_currency}&include_last_updated_at=true'
        resposta = requests.get(url)
        json_resposta = resposta.json()
        
        if resposta.status_code == 200:
            
            dados_moeda = json_resposta.get(coin_id,None)
            preco_brl = dados_moeda.get(vs_currency,None)
            atualizado_em = dados_moeda.get('last_updated_at',None)
            
            return preco_brl, atualizado_em
        else:
            raise ValueError("API offline, tente novamente mais tarde.")

class TelegramBot:
    
    def __init__(self,token: str, chatID: int):
        self.chatID = chatID
        self.bot = telegram.Bot(token=token)
    
    def enviar_mensagem(self, mensagem: str, parse_mode: str = 'MARKDOWN'):
        self.bot.send_message(chat_id=self.chatID, text=mensagem, parse_mode=parse_mode)
        
        print("Mensagem enviada com sucesso")