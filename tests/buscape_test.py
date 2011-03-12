import unittest
from urllib2 import URLError, HTTPError
import sys

sys.path.insert(0, '..') 
from buscape import Buscape


class BuscapeTest(unittest.TestCase):

    def setUp(self):
        applicationID = '2b613573535a6d324874493d'
        self.b = Buscape(applicationID=applicationID)

    def test_applicationid_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'User ID must be specified', Buscape)
        
    def test_applicationid_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'User ID must be specified', Buscape, applicationID='')
        
    def test_url_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'URL must be specified', self.b.fetch_url)

    def test_url_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError,'URL must be specified', self.b.fetch_url, url='')          

    def test_wrong_url_must_return_not_found_error(self):
        self.assertRaisesRegexp(URLError, 'HTTP Error 404: Not Found',self.b.fetch_url, url='http://sandbox.buscape.org/service/findProductList/2b613573535a6d324874493d/?categoryId=123&keyword=xpto')                  
    
    def test_right_url_must_return_code_200(self):
        self.assertEquals(self.b.fetch_url(url='http://sandbox.buscape.com/service/findProductList/2b613573535a6d324874493d/?categoryId=123&keyword=xpto')['code'],200)
    
    def test_user_must_be_authenticated(self):
        self.assertRaisesRegexp(URLError, 'The request requires user authentication',self.b.fetch_url, url='http://sandbox.buscape.com/service/findProductList/a/?categoryId=123&keyword=xpto')             
    
    def test_cannot_make_search_without_username(self):
        self.assertRaisesRegexp(URLError, 'HTTP Error 404: Not Found',self.b.fetch_url, url='http://sandbox.buscape.com/service/findProductList/?categoryId=123&keyword=xpto')  
    
    
    def test_search_parameters_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'Both method and search parameter must be specified',self.b.search)  

    def test_search_parameters_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'Both method and search parameter must be specified',self.b.search, method='',parameter='')

    def test_search_method_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'Method must be specified',self.b.search, parameter='?categoryId=123&keyword=xpto')        

    def test_search_parameter_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'Parameter must be specified',self.b.search, method='findProductList')

    def test_search_cannot_use_any_method(self):
        self.assertRaisesRegexp(ValueError, 'Invalid method',self.b.search, method='findFreeMusic',parameter='?keyword=carequinha')        
     
    def test_to_use_search_user_must_be_authenticated(self):
        wrong = Buscape('bozo')
        self.assertRaisesRegexp(URLError, 'The request requires user authentication',wrong.search, method='findProductList',parameter='?keyword=chuveiro') 

        
    def test_find_category_parameters_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list)         

    def test_find_category_parameters_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list, keyword='', categoryID='')   

    def test_find_category_parameter_keyword_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list, keyword='')   
 
    def test_find_category_parameter_categoryid_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list, categoryID='')    
    
    def test_find_category_both_parameters_are_not_accepted(self):
        self.assertRaisesRegexp(ValueError, 'you must specify only keyword or categoryID. Both values aren\'t accepted',self.b.find_category_list, keyword='xxx', categoryID=999)


    def test_find_category_parameter_format_cannot_be_blank(self):
         self.assertRaisesRegexp(ValueError, 'the return format must be XML or JSON',self.b.find_category_list, keyword='xxx', format='')       
         
    def test_find_category_parameter_format_must_be_json_or_xml(self):
         self.assertRaisesRegexp(ValueError, 'the return format must be XML or JSON',self.b.find_category_list, keyword='xxx', format='letter')               

    def test_find_category_parameter_format_must_be_case_insensitive(self):
         self.assertEquals(self.b.find_category_list(categoryID=0, format='json')['code'],200)             
         
    def test_find_category_by_keyword_must_return_200(self):
         self.assertEquals(self.b.find_category_list(keyword='LG')['code'],200)    

    def test_find_category_by_keyword_must_return_data(self):
         self.assertTrue(self.b.find_category_list(keyword='LG')['data'] is not None)              

    def test_find_category_by_categoryId_must_return_200(self):
         self.assertEquals(self.b.find_category_list(categoryID=0)['code'],200)    
         
    def test_find_category_by_categoryId_must_return_data(self):
         self.assertTrue(self.b.find_category_list(categoryID=0)['data'] is not None)       


         
    def test_find_product_parameters_cannot_be_null(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list)
         
    def test_find_product_parameters_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list,keyword='',categoryID='')   

    def test_find_product_only_keyword_parameter_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list,keyword='')   

    def test_find_product_only_categoryid_parameter_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list,categoryID='')  

    def test_find_product_only_keyword_parameter_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular')['code'],200)  

    def test_find_product_only_keyword_parameter_must_return_data(self):
        self.assertTrue(self.b.find_product_list(keyword='celular')['data'] is not None)          
        
    def test_find_product_only_categoryid_parameter_must_return_200(self):
        self.assertEquals(self.b.find_product_list(categoryID=0)['code'],200)      

    def test_find_product_only_categoryid_parameter_must_return_data(self):
        self.assertTrue(self.b.find_product_list(categoryID=0)['data'] is not None)

    def test_find_product_only_categoryid_parameter_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list,categoryID='')

    def test_find_product_format_must_be_xml_or_json(self):
         self.assertRaisesRegexp(ValueError, 'the return format must be XML or JSON',self.b.find_product_list,categoryID=0, format='letter')     
     
    def test_find_product_format_must_be_case_insensitive(self):
       self.assertEquals(self.b.find_product_list(categoryID=0, format='json')['code'],200)  


    def test_find_product_results_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=None)  
       
    def test_find_product_results_cannot_be_less_than_1(self):
        self.assertRaisesRegexp(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=0)  
        
    def test_find_product_results_cannot_be_greater_than_1(self):
        self.assertRaisesRegexp(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=1000)
    
    def test_find_product_results_must_be_a_valid_integer(self):
        self.assertRaisesRegexp(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=1000) 
    
    def test_find_product_results_must_be_between_1_and_999(self):
        self.assertEquals(self.b.find_product_list(categoryID=0, results=20)['code'],200)  


    def test_find_product_page_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page=None)          
        
    def test_find_product_page_cannot_be_less_than_1(self):
        self.assertRaisesRegexp(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page=0)  
        
    def test_find_product_page_cannot_be_greater_than_1(self):
        self.assertRaisesRegexp(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page=1000)

    def test_find_product_page_must_be_a_valid_integer(self):
        self.assertRaisesRegexp(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page='A')
        
    def test_find_product_page_must_be_between_1_and_999(self):
        self.assertEquals(self.b.find_product_list(categoryID=0, page=20)['code'],200)  


        
    def test_find_product_minPrice_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'minimum price must be a valid number',self.b.find_product_list,categoryID=0, minPrice=None)       

    def test_find_product_minPrice_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'minimum price must be a valid number',self.b.find_product_list,categoryID=0, minPrice='')             
        
    def test_find_product_minPrice_cannot_be_less_than_zero(self):
        self.assertRaisesRegexp(ValueError, 'minimum price can not be negative',self.b.find_product_list,categoryID=0, minPrice=-0.1)                

    def test_find_product_maxPrice_cannot_be_none(self):
        self.assertRaisesRegexp(ValueError, 'maximum price must be a valid number',self.b.find_product_list,categoryID=0, maxPrice=None)       

    def test_find_product_maxPrice_cannot_be_blank(self):
        self.assertRaisesRegexp(ValueError, 'maximum price must be a valid number',self.b.find_product_list,categoryID=0, maxPrice='')             
        
    def test_find_product_maxPrice_cannot_be_less_than_zero(self):
        self.assertRaisesRegexp(ValueError, 'maximum price can not be negative',self.b.find_product_list,categoryID=0, maxPrice=-0.1)          

    def test_find_product_minPrice_cannot_greater_than_maxPrice(self):
        self.assertRaisesRegexp(ValueError, 'minimum price can not be greater than maximum price',self.b.find_product_list,categoryID=0, minPrice=1, maxPrice=0.9)

    def test_find_product_setting_minPrice_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', minPrice=200)['code'],200)         
 
    def test_find_product_setting_maxPrice_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', maxPrice=1200.50)['code'],200)    

    def test_find_product_setting_minPrice_and_maxPrice_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', minPrice=344.90, maxPrice=1200.50)['code'],200) 
  
    def test_find_product_setting_all_variables(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', categoryID=0, format='json',page=3, results=20, minPrice=344.90, maxPrice=1200.50)['code'],200)         
  
if __name__ == '__main__':
    unittest.main()