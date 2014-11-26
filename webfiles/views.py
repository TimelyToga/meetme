__author__ = 'Tim'
try: import simplejson as json
except ImportError: import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext, loader

import logging
from meetme import settings

def home(request):
  template = loader.get_template('home.html')
  context = RequestContext(request, {})
  return HttpResponse(template.render(context))