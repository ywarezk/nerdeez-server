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
from django.utils.html import format_html

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

class EnrollAdmin(admin.ModelAdmin):
    pass

class HwAdmin(admin.ModelAdmin):
    pass

class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'hw', 'file', 'size', 'flag', 'flag_message', 'download')
    list_editable = ('title',)
    
    def download(self, file):
        return format_html('<a href="{0}">Download</a>', file.file)
    download.allow_tags = True


#===============================================================================
# end admin models
#===============================================================================

#===============================================================================
# begin admin site regitration
#===============================================================================

admin.site.register(SchoolGroup, SchoolGroupAdmin)
admin.site.register(Flatpage, FlatpageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Enroll, EnrollAdmin)
admin.site.register(Hw, HwAdmin)
admin.site.register(File, FileAdmin)


#===============================================================================
# end admin site registration
#===============================================================================