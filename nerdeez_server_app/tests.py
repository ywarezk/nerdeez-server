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
        '''

#===============================================================================
# end testing
#===============================================================================