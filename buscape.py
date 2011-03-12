#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__="Igor Hercowitz"
__author__="Alê Borba"
__version__="v0.1.0"

from VMBuilder.log import format
from urllib2 import urlopen, Request, URLError, HTTPError

class Buscape():
    """
    Class for BuscaPé's API abstraction
    """
    
    def __init__(self,applicationID=None, country="BR"):
        if not applicationID:
            raise ValueError("User ID must be specified") 
            
        self.applicationID = applicationID

        self.environment = 'bws'
        
        if country is None:
            self.country = "BR"
        else:
            self.country = country
        
    
    def __fetch_url(self, url=None):
        if not url:
            raise ValueError("URL must be specified")
        
        try:
            resp = urlopen(url)
            data = resp.read()
            return dict(code=resp.code,data=data)
            
        except URLError, e:
            if e.code == 401:
                if self.environment == 'bws':
                    raise URLError("Your application is not approved yet")
                else:
                    raise URLError("The request requires user authentication")
            else:    
                raise URLError(e)

    
    def __search(self, method=None, parameter=None):
        if not method and not parameter:
            raise ValueError("Both method and search parameter must be specified")
        elif not method:
            raise ValueError("Method must be specified")
        elif not parameter:
            raise ValueError("Parameter must be specified")

        if self.environment != 'sandbox':
            self.environment = 'bws'

        req = "http://%s.buscape.com/service/%s/%s/%s/?%s" %(self.environment, method, self.applicationID, self.country, parameter)
        
        try:
            ret = self.__fetch_url(url=req)
            return ret    
            
        except URLError, e:
            raise URLError(e)

            
    def set_sandbox(self):
        """
        Define the environment test
        """
        self.environment = 'sandbox'


    def find_category_list(self, keyword=None, categoryID=None, format='XML'):
        """
        Método faz busca de categorias, permite que você exiba informações
	relativas às categorias. É possível obter categorias, produtos ou ofertas
	informando apenas um ID de categoria.
        """

        if format.upper() not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")
        
        if not keyword and (categoryID < 0 or categoryID is None or categoryID==''): 
            raise ValueError("keyword or categoryID option must be specified")
        elif keyword and categoryID:
            raise ValueError("you must specify only keyword or categoryID. Both values aren't accepted")    
        
        if keyword:          
            parameter = "keyword=%s" %keyword          
        else:
            parameter = "categoryId=%s" %categoryID    

        parameter = parameter + "&format=%s" %(format)

        ret = self.__search(method='findCategoryList', parameter=parameter)
       
        return ret        
        
    
    def find_product_list(self, keyword=None, categoryID=None, format='XML', results=10,
                            page=1, minPrice=0.0, maxPrice=0.0):
        """
        Método permite que você busque uma lista de produtos únicos
	utilizando o id da categoria final ou um conjunto de palavras-chaves
	ou ambos.
        """
                            
        if format.upper() not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")
        
        if not keyword and (categoryID < 0 or categoryID is None or categoryID==''):
            raise ValueError("keyword or categoryID option must be specified")
        
        if results not in range(1,999):
            raise ValueError("results must be a integer between 1 and 999")

        if page not in range(1,999):
            raise ValueError("page number must be a integer between 1 and 999")
              
        if minPrice is None or minPrice == '':
            raise ValueError("minimum price must be a valid number")
        elif minPrice < 0.0:
            raise ValueError("minimum price can not be negative")
            
        if maxPrice is None or maxPrice == '':
            raise ValueError("maximum price must be a valid number")
        elif maxPrice < 0.0:
            raise ValueError("maximum price can not be negative")     
        elif maxPrice > 0.0 and minPrice > maxPrice:
            raise ValueError("minimum price can not be greater than maximum price")
            
              
        if keyword and categoryID:
            parameter = "categoryId=%s&keyword=%s" %(categoryID, keyword)
        elif not categoryID:          
            parameter = "keyword=%s" %keyword          
        elif not keyword:
            parameter = "categoryId=%s" %categoryID    

        parameter = parameter + "&format=%s" %(format)

        ret = self.__search(method='findProductList', parameter=parameter)
       
        return ret


    def create_source_id(self, sourceName=None, publisherID=None, siteID=None, campaignList=None, token=None, format='XML'):
        """
        Serviço utilizado somente na integração do Aplicativo com o Lomadee.
	Dentro do fluxo de integração, o aplicativo utiliza esse serviço para
	criar sourceId (código) para o Publisher que deseja utiliza-lo.
	Os parâmetros necessários neste serviço são informados pelo próprio
	Lomadee ao aplicativo.
	No ambiente de homologação sandbox, os valores dos parâmetros podem ser
	fictícios pois neste ambiente este serviço retornará sempre o mesmo sourceId
	para os testes do Developer.
        """

        if format.upper() not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")

        if sourceName is None:
            raise ValueError("sourceName option must be specified")

        if publisherID is None:
            raise ValueError("publisherID option must be specified")

        if siteID is None:
            raise ValueError("siteID option must be specified")

        if token is None:
            raise ValueError("token option must be specified")

        if campaignList:
            parameter = "sourceName=%s&publisherId=%s&siteId=%s&campaignList=%s&token=%s&format=%s" %(sourceName,publisherID,siteID,campaignList,token,format)
        else:
            parameter = "sourceName=%s&publisherId=%s&siteId=%s&token=%s&format=%s" %(sourceName,publisherID,siteID,token,format)

        ret = self.__search(method='createSource/lomadee', parameter=parameter)

        return ret


    def find_offer_list(self, categoryID=None, productID=None, barcode=None, keyword=None, lomadee=False, format="XML"):
        """
        Método permite que você busque uma lista de produtos únicos
	utilizando o id da categoria final ou um conjunto de palavras-chaves
	ou ambos.
        ToDo: Implementar filtros
        """

        if format.upper() not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")

        if lomadee:
            method = 'findOfferList/lomadee'
        else:
            method = 'findOfferList'

        if categoryID and keyword:
            parameter = "categoryId=%s&keyword=%s" %(categoryID,keyword)
        elif categoryID:
            parameter = "categoryId=%s" %(categoryID)
        elif keyword:
            parameter = "keyword=%s" %(keyword)
        elif barcode:
            parameter = "barcode=%s" %(barcode)
        elif productID:
            parameter = "productId=%s" %(productID)
        else:
            raise ValueError("One parameter must be especified")

        parameter = parameter + "&format=%s" %(format)

        ret = self.__search(method=method, parameter=parameter)

        return ret


    def top_products(self, format="XML"):
        """
        Método que retorna os produtos mais populares do BuscaPé.
        ToDo: Implementar filtros
        """

        if format.upper() not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")

        method = "topProducts"

        parameter = "&format=%s" %(format)

        ret = self.__search(method=method,parameter=parameter)

        return ret


    def view_product_details(self, productID=None,format="XML"):
        """
        Método retorna os detalhes técnicos de um determinado produto.
        """

        if format.upper() not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")

        if not productID:
            raise ValueError('productID option must be especified')

        method = "viewProductDetails"

        parameter = "productId=%s&format=%s" %(productID,format)

        ret = self.__search(method=method,parameter=parameter)

        return ret