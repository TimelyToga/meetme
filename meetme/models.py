__author__ = 'Tim'

from django.db import models

class ButtonClick( models.Model ):
    click_time = models.DateTimeField( auto_now=True )
    animal = models.CharField( max_length=200 )