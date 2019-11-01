TRACK_TERMS =["trump"]
CSV_NAME = "tweets.csv"
TABLE_NAME = "data_sent"

try:
    from private import *

except Exception:
    print('need private.py with private information!')