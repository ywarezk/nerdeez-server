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
from django.contrib.auth.models import User
import os
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from nerdeez_server_app import settings
from smtplib import SMTPSenderRefused
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse
from django.db import models

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

class ContactusResource(NerdeezResource):
    '''
    when the user fills the contact us form
    '''
    class Meta(NerdeezResource.Meta):
        allowed_methods = ['post']
        queryset = Contactus.objects.all()
        
    def obj_create(self, bundle, request=None, **kwargs):
        '''
        will send the message to our mail
        '''
        #get params
        message = bundle.data['message']
        mail = bundle.data['mail']
        admin_mail = os.environ['ADMIN_MAIL']
        
        t = get_template('contact_us_email.html')
        html = t.render(Context({'mail': mail, 'message': message}))
        text_content = strip_tags(html)
        msg = EmailMultiAlternatives(u'Nerdeez contact us', text_content, settings.FROM_EMAIL_ADDRESS, [admin_mail])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send()
        except SMTPSenderRefused, e:
            raise ImmediateHttpResponse(response=http.HttpApplicationError({'status' : "error", 'message' : "failed to send mail"}))
        return super(ContactusResource, self).obj_create(bundle, request, **kwargs)
    
    def dehydrate(self, bundle):
        '''
        will return the appropriate response
        '''
        bundle.data = {'status': "success", 'message': ""}
            
        return bundle
    
#===============================================================================
# end teh actual rest api
#===============================================================================