__author__ = 'Tim'

from django.db import models
from concurrency.fields import AutoIncVersionField

from meetme import settings
from meetme.server import mongo_helper


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