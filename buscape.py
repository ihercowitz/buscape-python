#! /usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import urlopen, Request, URLError, HTTPError

class Buscape():

    url = "http://sandbox.buscape.com/service/"
    
    def __init__(self,applicationID=None, country="BR"):
        if not applicationID:
            raise ValueError("User ID must be specified") 
            
        self.applicationID = applicationID
        
        if country is None:
            self.country = "BR"
        else:
            self.country = country
        
    
    def fetch_url(self, url=None):        
        if not url:
            raise ValueError("URL must be specified")
        
        try:
            resp = urlopen(url)
            data = resp.read()
            return dict(code=resp.code,data=data)
            
        except URLError, e:
            if e.code == 401:
                raise URLError("The request requires user authentication")
            else:    
                raise URLError(e)
        
    
    
    def search(self, method=None, parameter=None):        
        if not method and not parameter:
            raise ValueError("Both method and search parameter must be specified")
        elif not method:
            raise ValueError("Method must be specified")
        elif not parameter:
            raise ValueError("Parameter must be specified")
        
        
        if method not in ["findProductList","findCategoryList"]:
            raise ValueError("Invalid method")
        
        req = self.url+'%s/%s/%s/%s' %(method, self.applicationID, self.country, parameter)
        
        try:
            ret = self.fetch_url(url=req)
            return ret    
            
        except URLError, e:
            raise URLError(e)
            
    
    def find_category_list(self, keyword=None, categoryID=None, format='XML'):        
        if format.upper() not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")
        
        
        if not keyword and (categoryID < 0 or categoryID is None or categoryID==''): 
            raise ValueError("keyword or categoryID option must be specified")
        elif keyword and categoryID:
            raise ValueError("you must specify only keyword or categoryID. Both values aren't accepted")    
        
        if keyword:          
            parameter = "?keyword=%s" %keyword          
        else:
            parameter = "?categoryId=%s" %categoryID    

        ret = self.search(method='findCategoryList', parameter=parameter)        
       
        return ret        
        
    
    def find_product_list(self, keyword=None, categoryID=None, format='XML', results=10,
                            page=1, minPrice=0.0, maxPrice=0.0):
                            
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
            parameter = "?categoryId=%s&keyword=%s" %(categoryID, keyword)
        elif not categoryID:          
            parameter = "?keyword=%s" %keyword          
        elif not keyword:
            parameter = "?categoryId=%s" %categoryID    

        ret = self.search(method='findProductList', parameter=parameter)       
       
        return ret