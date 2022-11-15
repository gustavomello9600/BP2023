import datetime
import babel.numbers

import pandas as pd
import pytz
import streamlit as st
import yfinance as yf

f"""
# O Mercado

Abaixo elencamos as principais empresas listadas na B3 pertencentes ao setor de moda com dados
atualizados em {datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo')).strftime("%d/%m/%Y às %H:%M")}.
"""

tickers = ['ALPA4', 'SOMA3', 'ARZZ3', 'VIVA3', 'AMAR3', 'GRND3', 'CEAB3', 'TECN3',
           'GUAR3', 'VULC3', 'TFCO4', 'LLIS3', 'CGRA4', 'CAMB3', 'MNDL3', 'LREN3']

empresas = [yf.Ticker(ticker + ".SA").info for ticker in tickers]

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
Sumarizando os dados acima, entendemos que o mercado de moda no Brasil movimenta ao menos 
{babel.numbers.format_currency(sum(faturamentos_anuais), "BRL", "¤ #,##0.00", locale="pt_BR")} anuais e
que podemos esperar um valor de mercado de 
{sum(valor_de_mercado/receita for receita, valor_de_mercado in zip(faturamentos_anuais, valores_de_mercado))
 /len(empresas):.2f}x a receita total da Bázico na ocasião de uma oferta pública de ações.
"""