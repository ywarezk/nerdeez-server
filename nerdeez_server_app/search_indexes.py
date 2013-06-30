'''
will search index the models for search
Created on Jun 29, 2013

@author: ywarezk
@copyright: nerdeez.com
@version: 1.0
'''
#===============================================================================
# begin imports
#===============================================================================

from haystack import indexes
from nerdeez_server_app.models import *
import datetime

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin abstract classes
#===============================================================================

class NerdeezIndex(indexes.SearchIndex, indexes.Indexable):
    '''
    used to index our models
    '''
    
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return University

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())

#===============================================================================
# end abstract classes
#===============================================================================

#===============================================================================
# begin indexes
#===============================================================================

class UniversityIndex(NerdeezIndex):
    '''
    index university model
    '''
    def get_model(self):
        return University

    
class FacultyIndex(NerdeezIndex):
    '''
    used to index faculty
    '''
    def get_model(self):
        return Faculty
    
class CourseIndex(NerdeezIndex):
    '''
    used to index faculty
    '''
    def get_model(self):
        return Course

#===============================================================================
# end indexes
#===============================================================================

