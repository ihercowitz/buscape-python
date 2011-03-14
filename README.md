BuscaPé Python
==============

Camada de abstração para a API do BuscaPé utilizando Python.

Requerimentos
--------------
Python 2.6 oo superior da serie 2.x

Ainda nao foi testado com a versao 3.x

Dependências
--------------
O BuscaPé Python tem as seguintes dependências:

- urllib2


Instalação
-------------
Existem dois modos:

- Copiar o arquivo buscape.py para dentro do seu projeto

- Executar o instalador da seguinte forma:
--------------------------------------------
    
    #dentro da pasta buscape-python execute
    python setup.py build
    sudo python setup.py install


Métodos disponíveis
--------------------

set_sandbox()
--------------
Define se a aplicação está rodando em ambiente de testes. O padrão é o ambiente de produçao.

find_category_list(keyword, categoryID, format)
------------------------------------------------------------
Método faz busca de categorias, permite que você exiba informações relativas às categorias. O formato padrão de retorno é XML e a outra opção disponível é JSON.
Deve ser passado o parâmetro keyword ou categoryID, os dois juntos não é suportado pela API

find_product_list(keyword, categoryID, format, lomadee, results, page, minPrice, maxPrice)
-----------------------------------------------------------------------------------------
Método permite que você busque uma lista de produtos únicos utilizando o id da categoria final ou um conjunto de palavras-chaves ou ambos.

create_source_id(sourceName, publisherID, siteID, campaignList, token, format)
-------------------------------------------------------------------------------------------------------------
Método utilizado somente na integração do Aplicativo com o Lomadee.
Dentro do fluxo de integração, o aplicativo utiliza esse serviço para criar sourceId (código) para o Publisher que deseja utiliza-lo.
Os parâmetros necessários neste serviço são informados pelo próprio Lomadee ao aplicativo.
No ambiente de homologação sandbox, os valores dos parâmetros podem ser fictícios pois neste ambiente este serviço retornará sempre o mesmo sourceId para os testes do Developer.

find_offer_list(categoryID, productID, barcode, keyword, lomadee, format, results, page, priceMin, priceMax, sort, medal)
-------------------------------------------------------------------------------
Método permite que você busque uma lista de produtos únicos utilizando o id da categoria final ou um conjunto de palavras-chaves ou ambos.

top_products(format, filterID, valueID)
-----------------------
Método que retorna os produtos mais populares do BuscaPé.

view_product_details(productID, format)
---------------------------------------------------
Método retorna os detalhes técnicos de um determinado produto.

view_seller_details(sellerID, format)
-------------------------------------------------
Método que retorna os detalhes de uma loja ou empresa como: endereços, telefones de contato e etc.

view_user_ratings(productID, format)
------------------------------------------
Método que retorna as avaliações dos usuários sobre um determinado produto.


Exemplo de uso:
-----------------

    #! /usr/bin/python
    # -*- coding: utf-8 -*-

    #importanto a lib
    from buscape import Buscape

    #Instanciando o objeto
    buscape = Buscape(applicationID='your_applicationID')

    #Retornando a categoria 77
    exemplo = buscape.find_category_list(categoryID=77)

    #Imprimindo
    print exemplo
