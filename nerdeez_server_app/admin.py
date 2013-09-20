'''
will hold the admin interface models
Created on Jun 20, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================
from django.contrib import admin
from nerdeez_server_app.models import *

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin admin models
#===============================================================================


class SchoolGroupAdmin(admin.ModelAdmin):
    pass

class FlatpageAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass


#===============================================================================
# end admin models
#===============================================================================

#===============================================================================
# begin admin site regitration
#===============================================================================

admin.site.register(SchoolGroup, SchoolGroupAdmin)
admin.site.register(Flatpage, FlatpageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


#===============================================================================
# end admin site registration
#===============================================================================