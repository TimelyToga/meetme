from django.conf.urls import patterns, include, url
from django.contrib import admin

import meetme.settings
from meetme.server import oauth

urlpatterns = patterns('',
    url(r'^$', 'webfiles.views.home'),
    url(r'^auth$', 'meetme'),
    url(r'^oauth2callback$', 'meetme.server.oauth.oauth2callback'),
    url(r'^_/user', include('meetme.user.urls')),


    url(r'^admin/', include(admin.site.urls)),
    ## DIRECTORIES
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': meetme.settings.JS_DIR}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': meetme.settings.CSS_DIR}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': meetme.settings.IMG_DIR}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': meetme.settings.CSS_DIR}),
    (r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': meetme.settings.IMG_DIR}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': meetme.settings.JS_DIR}),
    (r'^robots.txt$', 'django.views.static.serve', {'path': 'robots.txt', 'document_root': meetme.settings.STATIC_DIR, 'show_indexes': False} ),
    (r'^favicon.ico$', 'django.views.static.serve', {'path': 'favicon.ico', 'document_root': meetme.settings.STATIC_DIR, 'show_indexes': False} ),
)
