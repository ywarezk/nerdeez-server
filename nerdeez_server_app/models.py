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
# begin constants
#===============================================================================

SCHOOL_TYPES = (
    (1, "Course"),
    (2, "Faculty"),
    (3, "University"),
)

DEFAULT_SCHOOL_TYPE = 1

#===============================================================================
# end constants
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
        
#===============================================================================
# end models abstract classes
#===============================================================================

#===============================================================================
# begin tables - models
#===============================================================================
        
class SchoolGroup(NerdeezModel):
    '''
    an abstract class for groups of students like university, faculty, course
    '''
    # table columns
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=False, default="")
    image = models.ImageField(upload_to='group_profile_image', default=None, null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, default=None, related_name='university')
    school_type = models.IntegerField(choices = SCHOOL_TYPES, default = DEFAULT_SCHOOL_TYPE, blank=False, null=False)
    
    def __unicode__(self):
        return self.title
    
    @classmethod
    def search(cls, query):
        '''
        used for searching using contains
        @param query: string of the query to search
        @return: {QuerySet} all the objects matching the search
        '''
        
        return cls.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(parent__title__icontains=query) | 
            Q(parent__description__icontains=query)).order_by('title').distinct()
        
    
class Flatpage(NerdeezModel):
    '''
    the flatpage table
    '''
    title = models.CharField(max_length=250, blank=False, null=False, unique=True)
    html = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title
        

#===============================================================================
# end tables - models
#===============================================================================