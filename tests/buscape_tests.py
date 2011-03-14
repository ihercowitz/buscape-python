import unittest
from urllib2 import URLError, HTTPError
import sys

sys.path.insert(0, '..') 
from buscape import Buscape


class BuscapeTest(unittest.TestCase):

    def assertRaisesMessage(self, excClass, message, callableObj, *args, **kwargs):
        try:
            callableObj(*args, **kwargs)
        except excClass, e:
        
            if excClass == URLError:
                reason = e.reason
            else:
                reason = e.message
                
            if message is not None and reason == message:
                return True
            else:
                raise self.failureException, "\nMessage expected: %s \nMessage raised: %s" %(message, reason)
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            raise self.failureException, "%s not raised" % excName 



    def setUp(self):
        self.applicationID = '2b613573535a6d324874493d'
        self.b = Buscape(applicationID=self.applicationID)
        self.b.set_sandbox()
  
    def test_applicationid_cannot_be_none(self):
        self.assertRaisesMessage(ValueError, 'User ID must be specified', Buscape)
        
    def test_applicationid_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'User ID must be specified', Buscape, applicationID='')
    
    def test_application_has_not_been_approved(self):
        app = Buscape(applicationID=self.applicationID)
        self.assertRaisesMessage(URLError, 'Your application is not approved yet',app.find_category_list, keyword='xxx')
 
    def test_application_with_wrong_applicationID_and_country_None(self):
        app = Buscape(applicationID='xpto', country=None)
        app.set_sandbox()
        self.assertRaisesMessage(URLError, 'The request requires user authentication',app.find_category_list, keyword='xxx')        
    
    
    def test_find_category_parameters_cannot_be_none(self):
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list)         

    def test_find_category_parameters_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list, keyword='', categoryID='')   

    def test_find_category_parameter_keyword_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list, keyword='')   
 
    def test_find_category_parameter_categoryid_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_category_list, categoryID='')    
    
    def test_find_category_both_parameters_are_not_accepted(self):
        self.assertRaisesMessage(ValueError, 'you must specify only keyword or categoryID. Both values aren\'t accepted',self.b.find_category_list, keyword='xxx', categoryID=999)


    def test_find_category_parameter_format_cannot_be_blank(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.find_category_list, keyword='xxx', format='')       
         
    def test_find_category_parameter_format_must_be_json_or_xml(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.find_category_list, keyword='xxx', format='letter')               

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
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list)
         
    def test_find_product_parameters_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list,keyword='',categoryID='')   

    def test_find_product_only_keyword_parameter_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list,keyword='')   

    def test_find_product_only_categoryid_parameter_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'keyword or categoryID option must be specified',self.b.find_product_list,categoryID='')  

    def test_find_product_only_keyword_parameter_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular')['code'],200)  

    def test_find_product_only_keyword_parameter_must_return_data(self):
        self.assertTrue(self.b.find_product_list(keyword='celular')['data'] is not None)          
        
        
    def test_find_product_only_categoryid_parameter_must_return_200(self):
        self.assertEquals(self.b.find_product_list(categoryID=0)['code'],200)      

    def test_find_product_only_categoryid_parameter_must_return_data(self):
        self.assertTrue(self.b.find_product_list(categoryID=0)['data'] is not None)

        
    def test_find_product_both_keywork_and_categoryid_parameter_must_return_200(self):
        self.assertTrue(self.b.find_product_list(keyword='celular',categoryID=0)['code'],200)     
        
    def test_find_product_both_keywork_and_categoryid_parameter_must_return_data(self):
        self.assertTrue(self.b.find_product_list(keyword='celular',categoryID=0)['data'] is not None)        


    def test_find_product_format_must_be_xml_or_json(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.find_product_list,categoryID=0, format='letter')     
     
    def test_find_product_format_must_be_case_insensitive(self):
       self.assertEquals(self.b.find_product_list(categoryID=0, format='json')['code'],200)  


    def test_find_product_results_cannot_be_none(self):
        self.assertRaisesMessage(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=None)  
       
    def test_find_product_results_cannot_be_less_than_1(self):
        self.assertRaisesMessage(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=0)  
        
    def test_find_product_results_cannot_be_greater_than_1(self):
        self.assertRaisesMessage(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=1000)
    
    def test_find_product_results_must_be_a_valid_integer(self):
        self.assertRaisesMessage(ValueError, 'results must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, results=1000) 
    
    def test_find_product_results_must_be_between_1_and_999(self):
        self.assertEquals(self.b.find_product_list(categoryID=0, results=20)['code'],200)  


    def test_find_product_page_cannot_be_none(self):
        self.assertRaisesMessage(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page=None)          
        
    def test_find_product_page_cannot_be_less_than_1(self):
        self.assertRaisesMessage(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page=0)  
        
    def test_find_product_page_cannot_be_greater_than_1(self):
        self.assertRaisesMessage(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page=1000)

    def test_find_product_page_must_be_a_valid_integer(self):
        self.assertRaisesMessage(ValueError, 'page number must be a integer between 1 and 999',self.b.find_product_list,categoryID=0, page='A')
        
    def test_find_product_page_must_be_between_1_and_999(self):
        self.assertEquals(self.b.find_product_list(categoryID=0, page=20)['code'],200)  


        
    def test_find_product_minPrice_cannot_be_none(self):
        self.assertRaisesMessage(ValueError, 'minimum price must be a valid number',self.b.find_product_list,categoryID=0, minPrice=None)       

    def test_find_product_minPrice_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'minimum price must be a valid number',self.b.find_product_list,categoryID=0, minPrice='')             
        
    def test_find_product_minPrice_cannot_be_less_than_zero(self):
        self.assertRaisesMessage(ValueError, 'minimum price can not be negative',self.b.find_product_list,categoryID=0, minPrice=-0.1)                

    def test_find_product_maxPrice_cannot_be_none(self):
        self.assertRaisesMessage(ValueError, 'maximum price must be a valid number',self.b.find_product_list,categoryID=0, maxPrice=None)       

    def test_find_product_maxPrice_cannot_be_blank(self):
        self.assertRaisesMessage(ValueError, 'maximum price must be a valid number',self.b.find_product_list,categoryID=0, maxPrice='')             
        
    def test_find_product_maxPrice_cannot_be_less_than_zero(self):
        self.assertRaisesMessage(ValueError, 'maximum price can not be negative',self.b.find_product_list,categoryID=0, maxPrice=-0.1)          

    def test_find_product_minPrice_cannot_greater_than_maxPrice(self):
        self.assertRaisesMessage(ValueError, 'minimum price can not be greater than maximum price',self.b.find_product_list,categoryID=0, minPrice=1, maxPrice=0.9)

    def test_find_product_setting_minPrice_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', minPrice=200)['code'],200)         
 
    def test_find_product_setting_maxPrice_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', maxPrice=1200.50)['code'],200)    

    def test_find_product_setting_minPrice_and_maxPrice_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', minPrice=344.90, maxPrice=1200.50)['code'],200) 
  
    def test_find_product_using_lomadee_must_return_200(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', lomadee=True)['code'],200)        
  
    def test_find_product_setting_all_variables(self):
        self.assertEquals(self.b.find_product_list(keyword='celular', categoryID=0, format='json',page=3, results=20, minPrice=344.90, maxPrice=1200.50)['code'],200)         
   


    def test_create_source_id_sourceName_cannot_be_None(self):
        self.assertRaisesMessage(ValueError, 'sourceName option must be specified',self.b.create_source_id)

    def test_create_source_id_format_must_be_xml_or_json(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.create_source_id, format='letter')             

    def test_create_source_id_publisherID_cannot_be_None(self):
        self.assertRaisesMessage(ValueError, 'publisherID option must be specified',self.b.create_source_id, sourceName='xxx')

    def test_create_source_id_siteID_cannot_be_None(self):
        self.assertRaisesMessage(ValueError, 'siteID option must be specified',self.b.create_source_id, sourceName='xxx', publisherID='abc')

    def test_create_source_id_token_cannot_be_None(self):
        self.assertRaisesMessage(ValueError, 'token option must be specified',self.b.create_source_id, sourceName='xxx', publisherID='abc', siteID='def')

    def test_create_source_id_use_campaignList_as_parameter_must_return_code_200(self):
        self.assertEquals(self.b.create_source_id(sourceName='xxx', publisherID='abc', siteID='def', token='ghi', campaignList='jkl')['code'],200)
 
    def test_create_source_id_without_use_campaignList_as_parameter_must_return_code_200(self):
        self.assertEquals(self.b.create_source_id(sourceName='xxx', publisherID='abc', siteID='def', token='ghi')['code'],200)



    def test_find_offer_list_format_must_be_xml_or_json(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.find_offer_list, format='letter')      
        
    def test_find_offer_list_at_least_one_parameter_must_be_specified(self):
         self.assertRaisesMessage(ValueError, 'One parameter must be especified',self.b.find_offer_list)                  
 
    def test_find_offer_list_sort_value_must_be_valid(self):
         self.assertRaisesMessage(ValueError, 'The value in the sort parameter is not valid',self.b.find_offer_list,keyword='xpto', sort='reverse')

    def test_find_offer_list_medal_value_must_be_valid(self):
         self.assertRaisesMessage(ValueError, 'The value in the medal parameter is not valid',self.b.find_offer_list,keyword='xpto', medal='stone')     
         
    def test_find_offer_list_using_keyword_must_return_200(self):
         self.assertEquals(self.b.find_offer_list(keyword='xpto', sort='price', medal='gold')['code'],200)

    def test_find_offer_list_using_categoryID_must_return_200(self):
         self.assertEquals(self.b.find_offer_list(categoryID=0, sort='price', medal='gold')['code'],200)

    def test_find_offer_list_using_keword_and_categoryID_must_return_200(self):
         self.assertEquals(self.b.find_offer_list(keyword='xpto', categoryID=0, sort='price', medal='gold')['code'],200)         
         
    def test_find_offer_list_using_barcode_must_return_200(self):
         self.assertEquals(self.b.find_offer_list(barcode='1234', sort='price', medal='gold')['code'],200)

    def test_find_offer_list_using_productID_must_return_200(self):
         self.assertEquals(self.b.find_offer_list(productID='1234', sort='price', medal='gold')['code'],200)
         
    def test_find_offer_list_using_lomadee_must_return_200(self):
         self.assertEquals(self.b.find_offer_list(keyword='xpto', lomadee=True, sort='price', medal='gold')['code'],200)          
         
    def test_find_offer_list_using_all_parameters_must_return_200(self):
         self.assertEquals(self.b.find_offer_list(keyword='xpto', lomadee=True, results=10, page=1, priceMin=0.1, priceMax=10.00, sort='price', medal='gold')['code'],200)    


    def test_top_products_format_must_be_xml_or_json(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.top_products, format='letter')      

    def test_top_products_must_return_200(self):
         self.assertEquals(self.b.top_products(filterID='x', valueID='y')['code'],200)    
 

    def test_view_product_details_format_must_be_xml_or_json(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.view_product_details, format='letter')      

    def test_view_product_details_productID_must_be_valid(self):
         self.assertRaisesMessage(ValueError, 'productID option must be specified',self.b.view_product_details)                 
    def test_view_product_details_must_return_200(self):
         self.assertEquals(self.b.view_product_details(productID='y')['code'],200)   


    def test_view_seller_details_format_must_be_xml_or_json(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.view_seller_details, format='letter')      

    def test_view_seller_details_productID_must_be_valid(self):
         self.assertRaisesMessage(ValueError, 'sellerID option must be specified',self.b.view_seller_details)                
         
    def test_view_seller_details_must_return_200(self):
         self.assertEquals(self.b.view_seller_details(sellerID='y')['code'],200)    
      

    def test_view_user_ratings_format_must_be_xml_or_json(self):
         self.assertRaisesMessage(ValueError, 'the return format must be XML or JSON',self.b.view_user_ratings, format='letter')  
         
    def test_view_user_ratings_productID_must_be_valid(self):
         self.assertRaisesMessage(ValueError, 'productID option must be specified',self.b.view_user_ratings)                       
    def test_view_user_ratings_must_return_200(self):
         self.assertEquals(self.b.view_user_ratings(productID='y')['code'],200)    
   





    """
    Tests for method assertRaisesMessage.
    """
    def test_assertRaisesMessage(self):
        def _raise(e):
            raise e
        self.assertTrue(self.assertRaisesMessage(Exception, 'Error', _raise, Exception('Error')) )
        self.assertRaises(Exception, self.assertRaisesMessage, Exception, _raise, Exception('Error') )
        self.assertRaises(self.failureException, self.assertRaisesMessage, Exception, 'Not correct', _raise, Exception('Error') )        


        
   
if __name__ == '__main__':
    unittest.main()