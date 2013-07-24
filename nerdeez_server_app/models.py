'''
contains the db models
Created on June 21, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from django.db import models
import datetime
from django.db.models import Q

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin models abstract classes
#===============================================================================

class NerdeezModel(models.Model):
    '''
    this class will be an abstract class for all my models
    and it will contain common information
    '''
    creation_date = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    modified_data = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0), auto_now=True)
    
    class Meta:
        abstract = True
        
class SchoolGroup(NerdeezModel):
    '''
    an abstract class for groups of students like university, faculty, course
    '''
    # table columns
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=False, default="")
    image = models.ImageField(upload_to='group_profile_image', default=None, null=True, blank=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.title
    
    @classmethod
    def search(cls, query):
        '''
        used for searching using contains
        @param query: string of the query to search
        @return: {QuerySet} all the objects matching the search
        '''
        
        return cls.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('title')
        
#===============================================================================
# end models abstract classes
#===============================================================================

#===============================================================================
# begin tables - models
#===============================================================================

class University(SchoolGroup):
    '''
    the university table
    '''
    pass
    

    
    
class Course(SchoolGroup):
    '''
    the courses table
    '''
    university = models.ForeignKey('University', related_name='university', null=True, blank=True)
    
    @classmethod
    def search(cls, query):
        '''
        @see: SchoolGroup.search
        '''
        
        return cls.objects.filter(
                                   Q(title__icontains=query) | 
                                   Q(description__icontains=query) |
                                   Q(university__title__icontains=query) |
                                   Q(university__description__icontains=query)).order_by('title')
    
class Flatpage(NerdeezModel):
    '''
    the flatpage table
    '''
    title = models.CharField(max_length=250, blank=False, null=False, unique=True)
    html = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title
        
class Contactus(NerdeezModel):
    '''
    user created a contact us message
    '''
    
    mail = models.EmailField(default=None, blank=True, null=True)
    message = models.TextField(blank=False, null=False)
    
    def __unicode__(self):
        return "%s - %s" % (self.mail, self.message)

#===============================================================================
# end tables - models
#===============================================================================