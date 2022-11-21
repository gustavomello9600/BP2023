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
                          for i, (receita, valor_de_mercado)
                          in enumerate(zip(faturamentos_anuais, valores_de_mercado))
                          if tickers[i] != 'TFCO4'
                          )/len(empresas)

f"""
Sumarizando-lhes, entendemos que o mercado de moda no Brasil movimenta ao menos 
{em_real(receita_total)} anuais e que podemos esperar um valor de mercado de 
{múltiplo_de_receita:.2f}x a receita anual da Bázico na ocasião de uma oferta pública de ações.
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
Mantidas as mesmas taxas de crescimento anual do mercado e considerando uma inflação de 5,91% a.a.
(média dos últimos 5 anos), é possível ensaiar as seguintes projeções:
"""

inflação = 0.059124360928308084
market_share_de_moda_básica = faturamentos_anuais[1]/receita_total

anos = [0, 5, 10, 20]
TAM = [receita_total * (1 + cagr - inflação) ** t for t in anos]
SAM = [tam * market_share_de_moda_básica for tam in TAM]
SOM = [sam/2 for sam in SAM]

MS_Bázico = [0.0025, 0.01, market_share_de_moda_básica/2]
receita_anual_projetada = [tam * ms for tam, ms in zip(TAM[1:], MS_Bázico)]
EV_Bázico = [múltiplo_de_receita * rec for rec in receita_anual_projetada]

projeção_de_crescimento_de_mercado = pd.DataFrame({"Anos": anos,
                                                   "TAM": TAM,
                                                   "SAM": SAM,
                                                   "SOM": SOM,
                                                   "Market Share (%)": [None] + [100 * ms for ms in MS_Bázico],
                                                   "Receita Anual (BRL)": [None] + receita_anual_projetada,
                                                   "Valor de mercado": [None] + EV_Bázico
                                                   }).style.format(na_rep="-", thousands=".", decimal=",", precision=2)

projeção_de_crescimento_de_mercado


f"""Presumiu-se que o SAM, entendido como o segmento de moda básica, fosse aproximadamente igual a
{market_share_de_moda_básica*100:.2f}% do TAM. Este percentual corresponde ao atual *market share* do grupo SOMA, 
*holding* controladora da Hering.

Uma vez que a ambição da Bázico é se tornar o *player* dominante deste segmento, estima-se o SOM como 50% do segmento
de moda básica, isto é, 50% do SAM e {market_share_de_moda_básica*50:.2f}% do TAM.

As projeções de crescimento de receita consideram a evolução de DNVBs nacionais e internacionais e de marcas
tradicionais como a Reserva."""

market_share = st.slider("% de market share", 0.5, 50.0, value=1.0, step=0.5)
anos_para_o_futuro = st.slider("Anos para o futuro", 1, 40, value=10, step=1)

TAM = receita_total * (1 + cagr - inflação) ** (anos_para_o_futuro)
SAM = TAM * market_share_de_moda_básica
SOM = SAM/2

col1, col2, col3 = st.columns(3)
col1.metric("TAM", em_real(TAM/(10**9), False) + " Bi")
col2.metric("SAM", em_real(SAM/(10**9), False) + " Bi")
col3.metric("SOM", em_real(SOM/(10**9), False) + " Bi")
col1.metric("Receita anual", em_real((TAM * market_share/100)/(10**9), False) + " Bi")
col2.metric("Valor de mercado", em_real((múltiplo_de_receita * TAM * market_share/100)/(10**9), False) + " Bi")