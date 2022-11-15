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

f"""
Sumarizando-lhes, entendemos que o mercado de moda no Brasil movimenta ao menos 
{babel.numbers.format_currency(sum(faturamentos_anuais), "BRL", "¤ #,##0.00", locale="pt_BR")} anuais e
que podemos esperar um valor de mercado de 
{sum(valor_de_mercado/receita for receita, valor_de_mercado in zip(faturamentos_anuais, valores_de_mercado))
 /len(empresas):.2f}x a receita total da Bázico na ocasião de uma oferta pública de ações.
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

"""Desde 2017
"""