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
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

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
    image = models.ImageField(upload_to='group_profile_image')
    
    search_index = VectorField()
    
    objects = SearchManager(
        fields = ('title', 'description'),
        auto_update_search_field = True
    )
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.title
        
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

class Faculty(SchoolGroup):
    '''
    the faculty table
    '''
    university = models.ForeignKey('University', related_name = "university", null = True, blank = True)
    
    objects = SearchManager(
        fields = ('title', 'description', 'university.title', 'university.description'),
        auto_update_search_field = True
    )
    
class Course(SchoolGroup):
    '''
    the courses table
    '''
    faculty = models.ForeignKey('Faculty', related_name='faculty', null=True, blank=True)
    
    objects = SearchManager(
        fields = ('title', 'description', 'faculty.university.title', 'faculty.university.description', 'faculty.title', 'faculty.description'),
        auto_update_search_field = True
    )
    

#===============================================================================
# end tables - models
#===============================================================================