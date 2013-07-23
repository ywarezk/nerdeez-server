'''
For my TDD, bitch
Created on Jun 29, 2013

@author: ywarezk
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin testing
#===============================================================================

class ApiTest(ResourceTestCase):
    '''
    nerdeez backend tests will be written here
    '''
    fixtures = ['nerdeez_server_app']
    
    def test_school_group_search(self):
        '''
        run a search query in the school group
        1 - make sure search query technion in uni yields one result
        1.1 - make sure bullshit search returns null
        2 - make sure search query technion in faculty yields 2 result
        3 - make sure search query technion in course yields 2 result
        '''
        
        resp = self.api_client.get('/api/v1/university/', format='json', data={'search': 'technion'})
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 1)
        
        resp = self.api_client.get('/api/v1/university/', format='json', data={'search': 'sdghskod'})
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 0)
        
        resp = self.api_client.get('/api/v1/course/', format='json', data={'search': 'technion'})
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 2)
        
    def test_flatpage(self):
        '''
        make sure get command works on flatpage url
        '''
        resp = self.api_client.get('/api/v1/flatpage/', format='json', data={})
        self.assertHttpOK(resp)
        
    def test_contactus(self):
        '''
        test send mail
        '''
        resp = self.api_client.post('/api/v1/contactus/', format='json', data={'mail': 'mail', 'message': 'testmessage'})
        self.assertHttpApplicationError(resp)
        
        

#===============================================================================
# end testing
#===============================================================================