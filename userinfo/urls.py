__author__ = 'jyoti'

from django.conf.urls import patterns, include, url
import userinfo.views


urlpatterns = patterns('',
    url(r'^$', userinfo.views.index, name='home'),
    url(r'^api/signup/$', userinfo.views.rest_signup, name='signup_api'),
    url(r'^api/userinfo/$', userinfo.views.user_list, name='all_user_list'),
    url(r'^api/userinfo/(?P<pk>[0-9]+)/$', userinfo.views.user_detail, name='single_user_details'),
    )

