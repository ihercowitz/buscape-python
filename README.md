BuscaPé Python
==============
Camada de abstração para a API do BuscaPé utilizando Python


Dependências
--------------
O BuscaPé Python tem as seguintes dependências:

- urllib2


Instalação
-------------
Basta copiar a pasta da lib para dentro do seu projeto


Métodos disponíveis
--------------------

set_sandbox()
--------------
Define se a aplicação está rodando em ambiente de testes. O padrão é o ambiente de produçao.

find_category_list(self, keyword, categoryID, format)
------------------------------------------------------------
Método faz busca de categorias, permite que você exiba informações relativas às categorias. O formato padrão de retorno é XML e a outra opção disponível é JSON.
Deve ser passado o parâmetro keyword ou categoryID, os dois juntos não é suportado pela API

find_product_list(self, keyword, categoryID, format, results, page, minPrice, maxPrice)
-----------------------------------------------------------------------------------------
Método permite que você busque uma lista de produtos únicos utilizando o id da categoria final ou um conjunto de palavras-chaves ou ambos.


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