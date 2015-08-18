from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('userinfo.urls', namespace='User Info')),  # This will redirect all urls matching
                                                                 #  this regex to our web-application urls.
)
