'''
Created on Feb 20, 2013
will check for the jsonp flag and wrap everything for jsonp
@author: yariv
'''

#===============================================================================
# begin imports
#===============================================================================

import traceback
import sys
from django.conf import settings

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin modifying the response
#===============================================================================

class DebugConvertTastyPieToHtmlMiddleware(object):
    
    def process_response(self, request, response):

        # if request was successful => response code is in range 2XX
        if response.status_code < 200 or response.status_code >= 300:
            return response

        #return if you dont have format=jsonp
        if not 'format' in request.GET or request.GET['format'] != 'json':
            return response

        response.content = '<html><body>' + response.content + '</body></html>'
        # print dir(response.get('Content-Type'))
        response['Content-Type'] = 'text/html'
        # response.content_type = 'text/html'
        
        return response

#===============================================================================
# end modifying the response
#===============================================================================