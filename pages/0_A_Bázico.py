import pandas as pd
import streamlit as st
import graphviz

"""
# A Bázico

**Revolucionar a moda através de experiências únicas.**

Esta é a razão de ser da Bázico, uma marca que surgiu da ideia de que o dinheiro do cliente deve valer mais.

Um preço justo, bom para os dois lados, para produtos incríveis com uma excelente experiência de compra e a sensação
de fazer parte de algo maior. Assim se resume o pacote de valor entregue a cada cliente.

## Modelo de Negócios
A Bázico se enxerga como uma [*Digital Native Vertical Brand*](https://dunn.medium.com/digitally-native-vertical-brands-b26a26f2cf83)
, isto é, uma marca nascida em meio digital que distribui seus produtos diretamente para seus clientes
(e por isso é vertical).
Posicionamo-nos como *creators* e engajamos uma comunidade conectada em torno dos nossos
produtos disponibilizados através do site [sejabazico.com.br](sejabazico.com.br).

Da compra, inicia-se o seguinte *flywheel*:
"""

grafo = graphviz.Digraph()
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Entrega rápida")
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Perfume especial no produto")
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Embalagem bem apresentada")
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Mensagem de agradecimento")
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Cartão de desconto para recompra")
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Atesta qualidade do produto")
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Boa experiência de compra")
grafo.edge("Nova aquisição", "Boa experiência com a marca", label="Boa experiência de pós-venda")
grafo.edge("Boa experiência com a marca", "Encantamento")
grafo.edge("Nova aquisição", "Acumula Bazicash")
grafo.edge("Acumula Bazicash", "Encantamento", label="Compra produtos exclusivos")
grafo.edge("Encantamento", "Programa de indicação")
grafo.edge("Programa de indicação", "Acumula Bazicash", label="Efetiva indicação")
grafo.edge("Programa de indicação", "Nova aquisição", label="Gera indicação")
grafo.edge("Encantamento", "Nova aquisição", label="Recompra")

st.graphviz_chart(grafo, use_container_width=True)

faturamento_anual = (pd.DataFrame({"Ano": ["2020", "2021", "2022 (YTD)"],
                                   "Faturamento": [24274.26, 310535.35, 943085.58],
                                   "Crescimento YoY (%)": [None, 1179.27, 203.69]})
                                  .set_index("Ano")
                                  .style.format(na_rep="-", thousands=".", decimal=",", precision=2))

"""

Atualmente, a Bázico oferece produtos de moda básica masculina de alta qualidade em termos de materiais e modelagem.
Dentre o *mix* de ofertas, dispomos de camisetas tradicionas, de gola "V", de modelagem alongada, camisas sociais de
manga curta, camisas de gola polo ou gola padre e cuecas.


## Breve histórico
A marca nasceu em Aracaju no ano de 2020, tomou corpo de empresa no final de 2021 e tem crescido a um CAGR de 523,31%.
Em fevereiro de 2022, transferiu sua operação para uma sede própria, denominada de QG. Em setembro do mesmo ano, abriu
a primeira loja própria: a Houze. Em novembro de 2022, a Bázico é composta por 7 pessoas (incluindo os dois *founders*) 
e fatura uma média mensal de R$ 129.256,92 (considerando agosto, setembro e outubro).
"""

faturamento_anual

"""
## Público atendido

A proposta de valor atende qualquer homem que queira praticidade, conforto e estilo na sua forma de se vestir.
No entanto, direcionamos a comunicação da marca para 3 contextos principalmente: viagens, festas e empreendedorismo.
Entendemos que nossa atual base permeia as comunidades destes 3 ambientes.

## Principais Lideranças
Rafael Issa, CEO e fundador, trabalha com moda masculina há 7 anos atendendo clientes diretamente e absorvendo na ponta
as suas necessidades e anseios. Acumula uma experiência de 4 anos no mercado de ecommerce.

Matheus Aricawa, CMO e fundador, é o rosto da marca, responsável por todo o *marketing* e *branding*. É o principal
articulador da estratégia de marca como *creator*. Trouxe sua experiência e seu carisma construídos na carreira
pregressa de artista, tanto solo quanto em grupo, para conquistar a lealdade e a admiração dos atuais clientes.

## Competidores
O **player** mais bem estabelecido no mercado de moda básica como um todo é a Hering.

No segmento de moda masculina de maior padrão, enxergamos concorrentes na Aramis e na Oficina Reserva.

Em termos de modelos de negócios mais próximos ao da Bázico, enxergamos a Insider, a Minimal Club e a Simples, esta
última criada pela Reserva por ter enxergado uma grande oportunidade neste segmento.

Entendemos que nenhum destes, com uma possível e discutível exceção na Minimal Club, adotam a mesma estratégia combinada
de posicionamento de marca como *creator* que engaja uma comunidade e entrega ótimas experiências *omnichannel*.
Entendemos ainda que esta estratégia é nosso principal diferencial competitivo.

## Precificação
Os preços dos nossos produtos são entre 7% a 47% mais baratos do que os dos nossos concorrentes diretos para
os mesmos tipos de material. Isto se traduz em margens operacionais em torno de 30% em meses com pouco investimento
em expansão e em torno de 20% em meses onde considerável capital é investido em crescimento (a exemplo da abertura
da Houze, primeira loja física).
"""


