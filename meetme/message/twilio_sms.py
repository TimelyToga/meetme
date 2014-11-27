try: import simplejson as json
except ImportError: import json
import logging
import random

from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

import meetme.settings
import meetme.server.date
import meetme.queue.defer


client = TwilioRestClient(meetme.settings.TWILIO_ACCOUNT_SID, meetme.settings.TWILIO_ACCOUNT_TOKEN)


def send_sms_sync(to_phone, message, from_phone=None):
  if not from_phone:
    from_phone = random.choice(client.phone_numbers.list()).phone_number
  logging.debug('sending sms from: %s, to: %s, with payload: %s' % (from_phone, to_phone, message))

  if meetme.settings.DEBUG:
    logging.debug('pretending to send an sms to: %s' % to_phone)
    return

  if meetme.settings.ENVIRONMENT == 'staging':
    logging.debug('STAGING PRENTENDING TO SEND A SMS: %s' % to_phone)
    return

  try:
    message_returned = client.messages.create(from_=from_phone, to=to_phone, body=message)
    try:
      logging.debug('message sent: %s' % json.dumps(message_returned.__dict__))
    except:
      pass
  except TwilioRestException:
    logging.exception('issue with phone: %s (sent from %s)' % (to_phone, from_phone))
    return
  logging.debug('%s with message %s completed' % (to_phone, message))

def send_sms(to_phone, message, from_phone=None):
  meetme.queue.defer.enqueue(send_sms_sync, to_phone, message, from_phone=from_phone)
