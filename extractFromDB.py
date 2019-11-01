import settings
import tweepy
import dataset
from datafreeze import freeze
# from textblob import TextBlob
print('ss',settings.CONNECTION_STRING)
print('csv name: ',settings.CSV_NAME)
print('table name: ',settings.TABLE_NAME)

db = dataset.connect(settings.CONNECTION_STRING)

res = db[settings.TABLE_NAME].all()

freeze(res, format='csv', filename=settings.CSV_NAME)