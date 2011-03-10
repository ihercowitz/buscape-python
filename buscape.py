#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import urlopen, Request, URLError, HTTPError

class Buscape():

    url = "http://sandbox.buscape.com/service/"
    
    def __init__(self,userID=None):

        
        if not userID:
            raise ValueError("User ID must be specified") 
            
        self.userID = userID
    
    
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
                print e
        
    
    def search(self, method=None, parameter=None):

        
        if not method and not parameter:
            raise ValueError("Both method and search parameter must be specified")
        elif not method:
            raise ValueError("Method must be specified")
        elif not parameter:
            raise ValueError("Parameter must be specified")
        
        
        if method not in ["findProductList","findCategoryList"]:
            raise ValueError("Invalid method")
        
        req = self.url+'%s/%s/%s' %(method, self.userID, parameter)      
        
        try:
            ret = self.fetch_url(url=req)
            return ret    
            
        except URLError, e:
            raise URLError(e)
            
    
    def find_category_list(self, keyword=None, categoryID=None, format='XML'):        
        if format not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")
        
        if not keyword and not categoryID:
            raise ValueError("keyword or caregoryID option must be specified")
        elif keyword and categoryID:
            raise ValueError("you must specify only keyword or categoryID. Both values aren't accepted")    
        
        if keyword and categoryID:
            parameter = "?categoryId=%s&keyword=%s" %(categoryID, keyword)
        elif not categoryID:          
            parameter = "?keyword=%s" %keyword          
        elif not keyword:
            parameter = "?categoryId=%s" %categoryID    

        ret = self.search(method='findCategoryList', parameter=parameter)        

       
        return ret        
        
    
    def find_product_list(self, keyword=None, categoryID=None, format='XML', results=10,
                            page=1):        
        if format not in ["XML","JSON"]:
            raise ValueError("the return format must be XML or JSON")
        
        if not keyword and not categoryID:
            raise ValueError("keyword or caregoryID option must be specified")
        
        if results not in range(1,999):
            raise ValueError("results must be a integer between 1 and 999")

        if page not in range(1,999):
            raise ValueError("page number must be between 1 and 999")
            
        if keyword and categoryID:
            parameter = "?categoryId=%s&keyword=%s" %(categoryID, keyword)
        elif not categoryID:          
            parameter = "?keyword=%s" %keyword          
        elif not keyword:
            parameter = "?categoryId=%s" %categoryID    

        ret = self.search(method='findProductList', parameter=parameter)       
       
        return ret
        
    
    
def __buscape_doctest():
    r"""

    ### Testing constructor ###
    >>> wrong = Buscape() #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: User ID must be specified
    
    
    ### Setting variables and constructor ###
    >>> userID = '2b613573535a6d324874493d'
    >>> b = Buscape(userID=userID)
    

    ### Testing fetch_url ###
    >>> b.fetch_url()  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: URL must be specified

    >>> b.fetch_url('')  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: URL must be specified

    >>> b.fetch_url('http://sandbox.buscape.com/service/findProductList/%s/?categoryId=123&keyword=xpto')['code'] %userID #doctest: +IGNORE_EXCEPTION_DETAIL
    200
 
    >>> b.fetch_url('http://sandbox.buscape.org/service/findProductList/%s/?categoryId=123&keyword=xpto') %userID #doctest: +IGNORE_EXCEPTION_DETAIL
    HTTP Error 404: Not Found

    >>> b.fetch_url('http://sandbox.buscape.com/service/findProductList/abc/?categoryId=123&keyword=xpto') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    URLError: The request requires user authentication    
    
    
    ### Testing search ###
    >>> b.search()  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Both method and search parameter must be specified

    >>> b.search('','')  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Both method and search parameter must be specified
    
    >>> b.search(parameter='?categoryId=123&keyword=xpto')  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Method must be specified        

    >>> b.search('',parameter='?categoryId=123&keyword=xpto')  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Method must be specified        
    
    >>> b.search(method='findProductList')  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Parameter must be specified       

    >>> b.search(method='findProductList', parameter='')  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Parameter must be specified 

    >>> b.search(method='findFreeMusic')  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Invalid method            
                  
    >>> wrong = Buscape(userID='2b6134874493d') 
    >>> wrong.search(method='findProductList', parameter='?categoryId=123&keyword=xpto') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    URLError: The request requires user authentication    
    
    
    ### Testing find_category_list ###
    >>> b.find_category_list() #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified         

    >>> b.find_category_list(keyword='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified   
    
    >>> b.find_category_list(categoryID='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified    

    >>> b.find_category_list(keyword='', categoryID='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified           
    
    >>> b.find_category_list(keyword='XXX', categoryID=999) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: you must specify only keyword or categoryID. Both values aren't accepted                   
    
    >>> b.find_category_list(keyword='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Parameter option must be specified                  
    
    >>> b.find_category_list(keyword='keyword',format='XXX') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON  
    
    >>> b.find_category_list(keyword='keyword',format='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON  
    
    >>> b.find_category_list(keyword='',format='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON
    
    >>> b.find_category_list(categoryID=999,format='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON  
    
    >>> b.find_category_list(categoryID=999,format='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON
    
    >>> b.find_category_list(keyword='LG')['code']
    200
   
   
    ### Testing find_category_list ###
    >>> b.find_product_list() #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified         

    >>> b.find_product_list(keyword='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified   
    
    >>> b.find_product_list(categoryID='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified    

    >>> b.find_product_list(keyword='', categoryID='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: keyword or caregoryID option must be specified           
    
    >>> b.find_product_list(keyword='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Parameter option must be specified                  
    
    >>> b.find_product_list(keyword='keyword',format='XXX') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON  
    
    >>> b.find_product_list(keyword='keyword',format='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON  
    
    >>> b.find_product_list(keyword='',format='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: the return format must be XML or JSON  
    
    >>> b.find_product_list(keyword='keyword',results='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999          
    
    >>> b.find_product_list(keyword='keyword',results='XYZ') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999           
    
    >>> b.find_product_list(keyword='keyword',results=None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999           
    
    >>> b.find_product_list(keyword='keyword',results=0) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999           
    
    >>> b.find_product_list(keyword='keyword',results=1000) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999   
   
    >>> b.find_product_list(keyword='celular',results='15')['code'] #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999

    >>> b.find_product_list(keyword='keyword',page=None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999           
    
    >>> b.find_product_list(keyword='keyword',page='') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999          
     
    >>> b.find_product_list(keyword='keyword',page=0) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999           
    
    >>> b.find_product_list(keyword='keyword',page=1000) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999   
    
    >>> b.find_product_list(keyword='keyword',page='XYZ') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999     
    
    >>> b.find_product_list(keyword='celular',page='15')['code'] #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: results must be a integer between 1 and 999
    
    >>> b.find_product_list(keyword='celular')['code']
    200
    
    >>> b.find_product_list(keyword='celular',results=15)['code']
    200
    
    >>> b.find_product_list(keyword='celular',page=15)['code']
    200
        
    """   
 