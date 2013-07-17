'''
Tastypie will play with this file to create a rest server
Created on Jun 20, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from nerdeez_server_app.models import *

#===============================================================================
# end imports
#===============================================================================


#===============================================================================
# begin abstract resources
#===============================================================================

class NerdeezResource(ModelResource):
    '''
    abstract class with commone attribute common to all my rest models
    '''
    
    #set read only fields
    class Meta:
        allowed_methods = ['get']
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        ordering = ['title']
        excludes = ['search_index']
        
class SchoolGroupResource(NerdeezResource):
    '''
    abstract class for common rest stuff for a school group: university, faculty, model
    '''
    
    class Meta(NerdeezResource.Meta):
        allowed_methods = ['get', 'post']
        
    def get_object_list(self, request):
        '''
        search group logic
        '''
        ids = []
        if request.GET.get('search') != None:
            search_object_list = self.Meta.object_class.search(request.GET.get('search'))
            [ids.append(obj.id) for obj in search_object_list]
            object_list = super(SchoolGroupResource, self).get_object_list(request)
            object_list = object_list.filter(id__in=ids)
        else:
            object_list = super(SchoolGroupResource, self).get_object_list(request)
        return object_list

#===============================================================================
# end abstract resources
#===============================================================================

#===============================================================================
# begin the actual rest api
#===============================================================================

class UniversityResource(SchoolGroupResource):
    '''
    the rest api for the university
    '''
    
    class Meta(SchoolGroupResource.Meta):
        queryset = University.objects.all()
        
        
class CourseResource(SchoolGroupResource):
    '''
    the rest api for the university
    '''
    university =  fields.ToOneField(UniversityResource, 'university', full=True, null=True)
    
    class Meta(SchoolGroupResource.Meta):
        queryset = Course.objects.all()
        
class FlatpageResource(NerdeezResource):
    '''
    the rest api for the flatpage
    '''
    class Meta(NerdeezResource.Meta):
        queryset = Flatpage.objects.all()
        filtering = {
                     'title': ALL,
                     }

#===============================================================================
# end teh actual rest api
#===============================================================================