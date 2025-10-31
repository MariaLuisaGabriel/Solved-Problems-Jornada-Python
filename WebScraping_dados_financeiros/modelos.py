#==============================================================
# Classe FundoImobiliario, representa um FII da tabela do Fundamentus
#==============================================================

class FundoImobiliario:
    def __init__(self, codigo, segmento, cotacao_atual, ffo_yield,
                    dividend_yield, p_vp, valor_mercado, liquidez, qt_imoveis, preco_m2,
                    aluguel_m2, cap_rate, vacancia_media):
        self.codigo = codigo
        self.segmento = segmento
        self.cotacao_atual = cotacao_atual
        self.ffo_yield = ffo_yield
        self.dividend_yield = dividend_yield
        self.p_vp = p_vp
        self.valor_mercado = valor_mercado
        self.liquidez = liquidez
        self.qt_imoveis = qt_imoveis
        self.preco_m2 = preco_m2
        self.aluguel_m2 = aluguel_m2
        self.cap_rate = cap_rate
        self.vacancia_media = vacancia_media

    def __repr__(self):
        return (f"FundoImobiliario(codigo={self.codigo}, nome={self.nome}, "
                f"setor={self.setor}, segmento={self.segmento}, "
                f"valor_cota={self.valor_cota}, liquidez_diaria={self.liquidez_diaria})")



#==============================================================
# Classe Estrategia, filtragem da tabela de FIIs
#==============================================================

class Estrategia:
    def __init__(self,segmento="",cotacao_atual_min=0.0, ffo_yield_min=0.0, dividend_yield_min=0.0,p_vp_min=0.0,
                    valor_mercado_min=0.0, liquidez_min=0.0, qt_imoveis_min=0, preco_m2_min=0.0,
                    aluguel_m2_min=0.0, cap_rate_min=0.0, vacancia_media_max=0.0):
        self.segmento = segmento
        self.cotacao_atual_min = cotacao_atual_min
        self.ffo_yield_min = ffo_yield_min
        self.dividend_yield_min = dividend_yield_min
        self.p_vp_min = p_vp_min
        self.valor_mercado_min = valor_mercado_min
        self.liquidez_min = liquidez_min
        self.qt_imoveis_min = qt_imoveis_min
        self.preco_m2_min = preco_m2_min
        self.aluguel_m2_min = aluguel_m2_min
        self.cap_rate_min = cap_rate_min
        self.vacancia_media_max = vacancia_media_max
    
    def aplicaEstrategia(self, fundo: FundoImobiliario):
        if self.segmento:
            if fundo.segmento != self.segmento:
                return False
        
        if fundo.cotacao_atual < self.cotacao_atual_min \
            or fundo.ffo_yield < self.ffo_yield_min \
            or fundo.dividend_yield < self.dividend_yield_min \
            or fundo.p_vp < self.p_vp_min \
            or fundo.valor_mercado < self.valor_mercado_min \
            or fundo.liquidez < self.liquidez_min \
            or fundo.qt_imoveis < self.qt_imoveis_min \
            or fundo.preco_m2 < self.preco_m2_min \
            or fundo.aluguel_m2 < self.aluguel_m2_min \
            or fundo.cap_rate < self.cap_rate_min \
            or fundo.vacancia_media > self.vacancia_media_max:
            
            return False
        
        return True