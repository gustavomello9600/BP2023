import datetime
import pickle
from pathlib import Path

import babel.numbers

import pandas as pd
import pytz
import streamlit as st
import yfinance as yf


arquivo_de_cache = Path("cache_de_dados_de_mercado")
tickers = ['ALPA4', 'SOMA3', 'ARZZ3', 'VIVA3', 'AMAR3', 'GRND3', 'CEAB3', 'TECN3',
           'GUAR3', 'VULC3', 'TFCO4', 'LLIS3', 'CGRA4', 'CAMB3', 'MNDL3', 'LREN3']


def em_real(x, escapar_cifrão=True):
    if escapar_cifrão:
        return "R\$" + babel.numbers.format_currency(x, "BRL", "¤ #,##0.00", locale="pt_BR")[2:]
    else:
        return babel.numbers.format_currency(x, "BRL", "¤ #,##0.00", locale="pt_BR")


if arquivo_de_cache.exists():
    with open(arquivo_de_cache, "rb") as cache:
        última_atualização, empresas, preços_históricos_de_ações = pickle.load(cache)
else:
    última_atualização = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo')).strftime("%d/%m/%Y às %H:%M")

    empresas = [yf.Ticker(ticker + ".SA").info for ticker in tickers]

    preços_históricos_de_ações = yf.download([ticker + ".SA" for ticker in tickers], '2017-1-1')["Adj Close"]

    with open(arquivo_de_cache, "wb") as cache:
        pickle.dump((última_atualização, empresas, preços_históricos_de_ações), cache)

f"""
# O Mercado

Abaixo elencamos as principais empresas listadas na B3 pertencentes ao setor de moda com dados
atualizados em {última_atualização}.
"""

nomes = [empresa['longName'] for empresa in empresas]
faturamentos_anuais = [empresa['totalRevenue'] for empresa in empresas]
valores_de_mercado = [empresa['enterpriseValue'] for empresa in empresas]

dados_do_setor = pd.DataFrame({"Ticker": tickers,
                               "Empresa": nomes,
                               "LTM": faturamentos_anuais,
                               "Valor de mercado": valores_de_mercado}
                              ).set_index("Ticker"
                              ).style.format(na_rep="-", thousands=".", decimal=",", precision=2)

dados_do_setor

receita_total = sum(faturamentos_anuais)
múltiplo_de_receita = sum(valor_de_mercado/receita
                          for receita, valor_de_mercado
                          in zip(faturamentos_anuais, valores_de_mercado)
                          )/len(empresas)

f"""
Sumarizando-lhes, entendemos que o mercado de moda no Brasil movimenta ao menos 
{em_real(receita_total)} anuais e que podemos esperar um valor de mercado de 
{múltiplo_de_receita:.2f}x a receita total da Bázico na ocasião de uma oferta pública de ações.
"""

preços_históricos_de_ações.columns = sorted(nomes, key=lambda nome: tickers[nomes.index(nome)])
preços_históricos_de_ações["Média do setor"] = preços_históricos_de_ações.mean(axis=1)

evolução_do_setor = (preços_históricos_de_ações
                     .rolling(window=90)
                     .mean())

"""## Crescimento
Média móvel de 90 dias do preço das ações do setor desde 2017 até a última atualização"""
para_analisar = st.multiselect("Quais ações comparar?", evolução_do_setor.columns, "Média do setor")
st.line_chart(evolução_do_setor[para_analisar])

f"""
Desde 2017, o preço médio das ações do setor saiu de {em_real((a := evolução_do_setor["Média do setor"].iloc[89]))} para
 {em_real((b := evolução_do_setor["Média do setor"].iloc[-1]))} o que representa um aumento de {100*(b/a - 1):.2f}%
ou ainda um CAGR de {100*(cagr := (b/a)**(1/5) - 1):.2f}%.


## TAM, SAM, SOM
Mantidas as mesmas taxas de crescimento anual do mercado e considerando uma inflação de 5,91% a.a. (média dos últimos 5 anos),
é possível ensaiar as seguintes projeções:
"""

inflação = 0.059124360928308084

anos = [5, 10, 20]
SAM = [receita_total * (1 + cagr - inflação)**t for t in anos]
MS_Bázico = [0.005, 0.01, 0.1]
SOM = [sam * ms for sam, ms in zip(SAM, MS_Bázico)]
EV_Bázico = [múltiplo_de_receita * som for som in SOM]

projeção_de_crescimento_de_mercado = pd.DataFrame({"Anos": anos,
                                                   "Mercado total endereçável": SAM,
                                                   "Market share alcançável (%)": [100 * ms for ms in MS_Bázico],
                                                   "Mercado total alcançável": SOM,
                                                   "Valor de mercado alcançável": EV_Bázico
                                                   }).style.format(na_rep="-", thousands=".", decimal=",", precision=2)

projeção_de_crescimento_de_mercado

market_share = st.slider("% de market share", 0.5, 50.0, value=1.0, step=0.5)
anos_para_o_futuro = st.slider("Anos para o futuro", 1, 40, value=5, step=1)

SAM = receita_total * (1 + cagr - inflação)**(anos_para_o_futuro)
SOM = SAM * market_share/100

col1, col2, col3 = st.columns(3)
col1.metric("Mercado total endereçável", em_real(SAM/(10**9), False) + " Bi")
col2.metric("Mercado total alcançável", em_real(SOM/(10**9), False) + " Bi")
col3.metric("Valor de mercado alcançável", em_real((SOM * múltiplo_de_receita)/(10**9), False) + " Bi")