# will use the event-driven: program executes actions based on external inputs.
# tweepy is the most popular library which allows user to connect to the streaming API and handle errors properly

# Opening for tweets / this connects our server or local computer to twitter api for streaming
# using firehose.json API endpoint will allow us to gather all tweets but costly. Thus, we will use filter.json API endpoint with some limitations(restricted size of tweets) - opening connection part. we will use python reqeusts library


# Listening for tweets
# once we open a connection, we need to listen for tweets from this connection. tweets will be sent as plain text data.
# HTTP connections header
# then json file format...

# Calling the callback
# once tweepy decodes the tweet data, we will pass the data to a preregistered callback function def _data.
#   self.listener will check whether data is good to go or not. If data is not good or does not match with the criteria, it wil shut down the connection.

import tweepy
import settings
import dataset
import json
from sqlalchemy.exc import ProgrammingError
import time

print('setting db dataset: ',settings.CONNECTION_STRING)
db = dataset.connect(settings.CONNECTION_STRING)


# multi thead in python ( 비동기 처리..라고한다. 동기처리는 그냥 보통 라인바이라인 순서대로 실행)
# 리슨하는 와중에 어레이 100개 차면 sqs로 보낼건데(lambd를 이용해서 혹은 EC2 ! ),
#   보낼때도 안전하게 데이타를 잘 리슨하고싶다
#       즉, arr.append()용 스레드1, send_arr_to_sqs()용 스레드2 를 어떻게 구현하는지 알아봐라
# !!! 프로세스와 스레드가 뭐가다른지도 찾아봐 <- 좀 어려울거임.

class StreamListener(tweepy.StreamListener):
    # use the super to call the original __init__,
    # and wrap the file I/O in a with statement
    def __init__(self):
        super(StreamListener, self).__init__()
        print('hi added~! now we can modify init !')

    def isUseless(self, status):
        return True if len(status.text) < 10 else False

    def on_status(self, status):
        if self.isUseless(status):
            return

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = json.dumps(status.coordinates) if status.coordinates else None
        geo = json.dumps(status.geo) if status.geo else None # takes an object and produces a string
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        # blob = TextBlob(text)
        # sent = blob.sentiment

        # print('below is status.text')
        print(status.text)

        table = db[settings.TABLE_NAME]

        try:
            # db에 쌓는거 대신에,
            # self.temp_arr.append(each tweet object)
            # self.len_temp_arr += 1
            tweet_dict = dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                geo=geo,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                # polarity=sent.polarity,
                # subjectivity=sent.subjectivity,
            )
            table.insert(tweet_dict)
        except ProgrammingError as err:
            print(err)

        # # read: 디비에 요청을 한번더 보내야해.. <- costly
        # # 한 process에서 read, write다하면 느리다.
        # # if table.count() % 100 == 0:
        # if self.len_temp_arr % 100 == 0:
        #     # send temp_Arr to SQS!!!!!!!
        #     # self.temp_arr = []
        #     # self.len_temp_arr = 0


    def on_error(self, status_code):
        '''
        return False to disconnects the stream if our connections reaches to the limit
        Rate limiting and other concerns
        tweepy handles the rate limits, prohibition on the # of connection attempts from same authorization keys
        Attention: If we take too long to process tweets, they will start to get queued, and twitter may disconnect our CONNECTION. -> We need to process each tweet extremly fast.

        :param self:
        :param status_code:
        :return:
        '''
        if status_code == 420: return False



#
# def filter_tweet(tweet):
#     '''
#     remove any tweets that do not match the criteria
#     This is CALLBACK with streamer which gets the tweet in real-time
#     This will be called every time as receiving the new tweet
#     Then process_tweet or store_tweet will be called
#     :param tweet:
#     :return:
#     '''
#
#     if not tweet_mateches_critera(tweet):
#         return
#
#
# # process the remaining tweet)
# process_tweet(tweet)
#
# def process_tweet(tweet):
#     '''
#     update the tweet dictionary with any other information we need
#     :param tweet:
#     :return:
#     '''
#
#     tweet['sentiment'] = get_sentiment(tweet)
#
# # Store the tweet
# store_tweet(tweet)
#
# def store_tweet(tweet):
#     '''
#     save a tweet for later processing
#     :param tweet:
#     :return:
#     '''