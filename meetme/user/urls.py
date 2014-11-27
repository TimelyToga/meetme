__author__ = 'Tim'
from django.conf.urls import patterns, url

urlpatterns = patterns('meetme.user.handler',
  url(r'^/sign_in$', 'sign_in'),
  url(r'^/creat_user$', 'create_user'),
  )
