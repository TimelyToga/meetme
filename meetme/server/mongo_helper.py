__author__ = 'Tim'

from meetme import settings
from pymongo import MongoClient


def get_cal_database():
  client = MongoClient(settings.MONGODB_URI)
  db = client[settings.DB_NAME]
  return db[settings.MAIN_COLLECTION_NAME]