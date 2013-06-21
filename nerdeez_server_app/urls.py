from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nerdeez_server_app.views.home', name='home'),
    # url(r'^nerdeez_server_app/', include('nerdeez_server_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    ('^$', nerdeez_server_app.views.porthole),
    ('^proxy/', nerdeez_server_app.views.proxy),
)
