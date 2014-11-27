import time
from datetime import datetime

import camoji.common.date


def make_timestamp_in_ms(datetime):
  if not datetime:
    return None
  return int(time.mktime(datetime.timetuple()) * 1000)


def pretty_ago(start_time=None, time=None):
  diff = pretty_diff(start_time=start_time, time=time)
  return ('%s ago' % diff) if diff else ''


def pretty_diff(start_time=None, time=None):
  if not time:
    return ''
  if not start_time:
    start_time = camoji.common.date.datetime.utcnow()
  if type(start_time) is int and type(time) is int:
    diff = datetime.fromtimestamp(start_time) - datetime.fromtimestamp(time)
  elif isinstance(start_time, datetime) and isinstance(time, datetime):
    diff = start_time - time
  else:
    diff = start_time - time

  millisecond_diff = diff.microseconds / 1000
  second_diff = diff.seconds
  day_diff = diff.days

  if day_diff < 0:
    return ''

  if day_diff == 0:
    if second_diff == 0:
      return str(millisecond_diff) + ' ms'
    if second_diff < 2:
      return str(second_diff) + ' second'
    if second_diff < 120:
      return str(second_diff) + ' seconds'
    if second_diff < 7200:
      return str( second_diff / 60 ) + ' minutes'
    if second_diff < 86400:
      return str( second_diff / 3600 ) + ' hours'
  if day_diff == 1:
    return str(day_diff) + ' day'
  if day_diff < 7:
    return str(day_diff) + ' days'
  if day_diff < 31:
    return str(day_diff / 7) + ' weeks'
  if day_diff < 365:
    return str(day_diff / 30) + ' months'
  return str(day_diff / 365) + ' years'

