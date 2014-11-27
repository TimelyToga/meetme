__author__ = 'Tim'

from meetme.server.response import JsonResponseBadRequest, JsonResponse, require_json_args
from meetme.user.models import User, Session
from django.db import transaction


import logging
import base64
import logging
import os
import re

import meetme.server.date

@require_json_args('username', 'password')
def sign_in(request):
  email_or_username = request.json['email_or_username']
  password = request.json['password']

  # check to see if this user is just trying to login
  user = User.user_from_username(email_or_username)
  if not user:
    user = User.user_from_email(email_or_username)

  if not user:
    return JsonResponse({})

  if not user.authenticate(password):
    logging.debug('wrong password for that user')
    return JsonResponse({})

  logging.info('Creating new session')
  session = Session()
  session.key = base64.urlsafe_b64encode(os.urandom(16))
  session.user = user
  session.created = meetme.server.date.datetime.utcnow()
  session.save()
  setattr(request, 'session', session)

  return JsonResponse(dict({'sid': session.pk}.items() + user.get_all_user_as_data(user).items()))

@require_json_args('email', 'username', 'password')
def create_user(request):
  email = request.json['email']
  username = request.json['username']
  password = request.json['password']

  if username != re.sub(r'[^a-zA-Z0-9_]+', '', username):
    return JsonResponseBadRequest('no valid username')

  user = User.user_from_username(username)
  if user:
    if user.authenticate(password):
      ## Log in
      print "logging in"

  with transaction.atomic():
    user = User()
    user.username = username
    user.email_pending = email
    user.set_and_encrypt_password(password)
    user.save()

    ## Create new Session