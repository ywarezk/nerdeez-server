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
from django.contrib.auth.models import User
from decimal import Decimal
import string
import random

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

class UserProfile(NerdeezModel):
    '''
    will hold the models for a user profile
    '''
    user = models.ForeignKey(User, unique=True)
    email_hash = models.CharField(max_length=100, blank = True, null = True, default="")
    twitter_oauth_token = models.CharField(max_length=255, blank = True, null = True, default="")
    twitter_oauth_token_secret = models.CharField(max_length=255, blank = True, null = True, default="")
    school_groups = models.ManyToManyField('SchoolGroup', related_name = "users", through = 'Enroll')
    
    def __unicode__(self):
        '''
        object description string
        @returns String: object description
        '''
        return self.user.email
    
def createHash():
    '''
    will return a random hash
    @return: random hash as string
    '''
    pool = string.letters + string.digits
    return ''.join(random.choice(pool) for i in xrange(64))

    
class ForgotPass(NerdeezModel):
    '''
    the table that holds hash and forgot password data
    '''
    
    user = models.ForeignKey(UserProfile)
    time = models.DateTimeField("time", default=lambda: datetime.datetime.now().replace(microsecond=0))
    hash = models.CharField(max_length=100 , default=createHash)
        
class SchoolGroup(NerdeezModel):
    '''
    an abstract class for groups of students like university, faculty, course
    '''
    # table columns
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=False, default="")
    parent = models.ForeignKey('self', blank=True, null=True, default=None, related_name='university')
    school_type = models.IntegerField(choices = SCHOOL_TYPES, default = DEFAULT_SCHOOL_TYPE, blank=False, null=False)
    grade = models.DecimalField(max_digits = 3, decimal_places = 1, default = Decimal("3.5"))
    
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


class Enroll(NerdeezModel):
    user = models.ForeignKey(UserProfile)
    school_group = models.ForeignKey(SchoolGroup)
    last_entered = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0), auto_now=True)
    
    class Meta:
        unique_together = (("user", "school_group"),) 
    
    def __unicode__(self):
        return '%s - %s' %(self.user.user.email, self.school_group.title)
    
          

#===============================================================================
# end tables - models
#===============================================================================

#===============================================================================
# begin signals
#===============================================================================

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

#===============================================================================
# end signals
#===============================================================================

