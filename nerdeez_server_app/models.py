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
from django.db.models.fields import CharField, IntegerField
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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

NUM_ENROLLED_COURSES = 10

REPUTATION_OPEN_SCHOOLGROUP = 10
REPUTATION_OPEN_HW = 100
REPUTATION_OPEN_FILE = 1000

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
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    
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

class UserProfile(NerdeezModel):
    '''
    will hold the models for a user profile
    '''
    user = models.ForeignKey(User, unique=True)
    email_hash = models.CharField(max_length=100, blank = True, null = True, default="")
    twitter_oauth_token = models.CharField(max_length=255, blank = True, null = True, default="")
    twitter_oauth_token_secret = models.CharField(max_length=255, blank = True, null = True, default="")
    school_groups = models.ManyToManyField('SchoolGroup', related_name = "users", through = 'Enroll')
    first_name = models.CharField(max_length=100, blank = True, null = True, default=None)
    last_name = models.CharField(max_length=100, blank = True, null = True, default=None)
    
    def __unicode__(self):
        '''
        object description string
        @returns String: object description
        '''
        return self.user.email
    
    def owner(self):
        return self.user
    
    def get_reputation(self):
        '''
        Will calculate the user reputation based on history
        @return: Integer positive number of the reputation
        '''
        result = 0
        
        #how many school groups did the user opened
        amount_schoolgroups = SchoolGroup.objects.filter(user_profile=self).count()
        result = result + (amount_schoolgroups * REPUTATION_OPEN_SCHOOLGROUP)
        
        #how many H.W did the user create
        amount_hw = Hw.objects.filter(user_profile=self).count()
        result = result + (amount_hw * REPUTATION_OPEN_HW)
        
        #how many Files did the user upload
        amount_files = File.objects.filter(user_profile=self).count()
        result = result + (amount_files * REPUTATION_OPEN_FILE)
        
        return result
    
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
    image = models.CharField(max_length=500, default=None, blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile, default=None, blank=True, null=True)
    
    search_index = VectorField()

    objects = SearchManager(
        fields = ('title', 'description'),
        config = 'pg_catalog.english', # this is default
        search_field = 'search_index', # this is default
        auto_update_search_field = True
    )
    
    @classmethod
    def search(cls, query):
        '''
        used for searching using contains
        @param query: string of the query to search
        @return: {QuerySet} all the objects matching the search
        '''
        
        return cls.objects.search(query).distinct()
        
    
class Flatpage(NerdeezModel):
    '''
    the flatpage table
    '''
    title = models.CharField(max_length=250, blank=False, null=False, unique=True)
    html = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.title


class Enroll(NerdeezModel):
    user = models.ForeignKey(UserProfile, related_name='enrolls')
    school_group = models.ForeignKey(SchoolGroup, related_name='link_to_schoolgroup')
    last_entered = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    
    class Meta:
        ordering = ['-last_entered']
        unique_together = (("user", "school_group"),) 
    
    def __unicode__(self):
        return '%s - %s' %(self.user.user.email, self.school_group.title)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        '''
        if i have more than ten for the user then need to delete some records
        '''
        result = super(Enroll, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        num_records = Enroll.objects.filter(user=self.user).count()
        if num_records > NUM_ENROLLED_COURSES:
            records = Enroll.objects.filter(user=self.user).order_by('last_entered')
            for i in range(0,num_records-NUM_ENROLLED_COURSES):
                records[i].delete()
                    
        return result
    
    def owner(self):
        return self.user.user
    
class Hw(NerdeezModel):
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=False, default="")
    school_group = models.ForeignKey(SchoolGroup, related_name='hws')
    user_profile = models.ForeignKey(UserProfile, default=None, blank=True, null=True)
    
    class Meta:
        ordering = ['title']
        
class File(NerdeezModel):
    title = models.CharField(max_length=250, blank=False, null=False)
    hw = models.ForeignKey(Hw, related_name='files', default=None, blank=True, null=True)
    file = models.CharField(max_length=500, default='', blank=True, null=True)    
    size = models.FloatField(default=0)
    hash = models.CharField(max_length=1000, blank=True, null=True)
    flag = models.BooleanField(default=False)
    flag_message = models.CharField(max_length=300, default='')
    user_profile = models.ForeignKey(UserProfile, default=None, blank=True, null=True)
    
    class Meta:
        ordering = ['title']
        
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in File._meta.fields]
    
class LikedItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    
          

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


