__author__ = 'Tim'

from django.db import models
from concurrency.fields import AutoIncVersionField

import meetme.server.date
import meetme.message.sendgrid_email
from meetme import settings
from meetme.server import mongo_helper
from pytz import timezone
from django.core.exceptions import ObjectDoesNotExist

import hashlib
import json
import logging
import datetime
import time

def encrypt(password, salt, hash_algorithm=hashlib.sha1):
  if not salt:
    raise Exception('need salt')
  to_encrypt = password + salt
  return hash_algorithm(to_encrypt).hexdigest()

class User(models.Model):
    pk = models.CharField(primary_key=True, max_length=256)
    username = models.CharField(max_length=50)
    salt = models.CharField(max_length=256, null=True)
    password = models.CharField(max_length=256, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_pending = models.CharField(max_length=256)
    email_confirmed = models.CharField(max_length=256)

    created = models.DateTimeField('created', db_index=True)
    version = AutoIncVersionField()

    def get_data(self):
      col = mongo_helper.get_cal_database()
      return col.find_one( { "id": self.pk } )

    def set_and_encrypt_password(self, password, salt=str(int(time.time()))):
      self.salt = salt
      self.password = encrypt(password, self.salt)

    def authenticate(self, password):
      if self.password == encrypt(password, self.salt):
        return True
      return False

    @staticmethod
    def user_from_username(username):
      try:
        return User.objects.get(username__iexact=username)
      except ObjectDoesNotExist:
        return None

    @staticmethod
    def user_from_phone(phone):
      try:
        return User.objects.get(phone_verified=phone)
      except ObjectDoesNotExist:
        return None

    @staticmethod
    def user_from_email(email):
      try:
        return User.objects.get(Q(email_pending=email) | Q(email_verified=email))
      except ObjectDoesNotExist:
        return None

class Session(models.Model):

  class Meta:
    db_table = 'meetme_session'

  key = models.CharField(primary_key=True, max_length=256)
  user = models.ForeignKey(User, related_name='+')
  user_agent = models.CharField(null=True, max_length=512)
  time_zone = models.CharField(null=True, max_length=512)
  created = models.DateTimeField('created', db_index=True)
  used = models.DateTimeField('used', null=True, db_index=True)
  deleted = models.BooleanField(default=False)

  @property
  def time_zone_obj(self):
    if not self.time_zone:
      return None
    return timezone(self.time_zone)

  def app_version(self):
    if not self.user_agent:
      return None
    return json.loads(str(self.user_agent))['app_version']

  def invalidate(self):
    self.deleted = True
    self.save()

  @staticmethod
  def invalidate_for_user(user, except_sessions=list()):
    except_sessions = set(except_sessions)
    # make sure all exception session are valid
    for session in except_sessions:
      if session.deleted:
        # if any are not valid, bail on entire request
        return
    latest_created = None
    for except_session in except_sessions:
      if not latest_created or except_session.created > latest_created:
        latest_created = except_session.created
    for session in Session.objects.filter(user=user, deleted=False):
      if session in except_sessions:
        # do not touch any sessions passed in except
        continue

      if session.created < latest_created:
        logging.info('invalidating session: %s and user: %s, %s' % (session.pk, user.pk, session.user_agent))
        session.invalidate()
        continue

      if not session.used:
        logging.info('invalidating session: %s and user: %s, %s' % (session.pk, user.pk, session.user_agent))
        session.invalidate()
        continue

      # session was created after but hasn't been used in 10 minutes
      hour_old = meetme.server.date.datetime.utcnow() - datetime.timedelta(minutes=10)
      if session.used < hour_old:
        logging.info('invalidating session: %s and user: %s, %s' % (session.pk, user.pk, session.user_agent))
        session.invalidate()
        continue

class EmailVerification(models.Model):
  class Meta:
    db_table = 'email_verification'

  user = models.ForeignKey(User, related_name='+')

  confirmation_code = models.CharField(db_index=True, max_length=256, unique=True)

  email = models.CharField(db_index=True, max_length=256)
  voided = models.DateTimeField('voided', null=True)
  completed = models.DateTimeField('completed', null=True)
  created = models.DateTimeField('created', db_index=True)

  def send(self):
    meetme.message.sendgrid_email.send_sync(to=self.email,
                                       from_address='support@camoji.com',
                                       subject='Camoji Email Verification',
                                       text_template='email-verification-email.txt',
                                       html_template='email-verification-email.html',
                                       web_host_url=meetme.settings.WWW_HOST_URL,
                                       token=self.confirmation_code)