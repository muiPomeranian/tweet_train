# from streamTweet_multiTHRD import StreamListener
from streamTweet import StreamListener
import argparse
import settings
import tweepy

def create_api(app_key = settings.TWITTER_APP_KEY,
               app_secret = settings.TWITTER_APP_SECRET,

               twitter_key = settings.TWITTER_KEY,
               twitter_secret = settings.TWITTER_SECRET):

    auth = tweepy.OAuthHandler(app_key, app_secret)
    auth.set_access_token(twitter_key, twitter_secret)
    api = tweepy.API(auth)

    return api


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app_key", default=None, type=str, required=False,
                        help="use your own TWITTER APP KEY")
    parser.add_argument("--app_secret", default=None, type=str, required=False,
                        help="use your own TWITTER APP SECRET")
    parser.add_argument("--twitter_secret", type=str, default=None,
                        help="use your TWITTER SECRET")
    parser.add_argument("--twitter_key", type=str, default=None,
                        help="use your TWITTER KEY")
    # parser.add_argument("--no_cuda", action='store_true',
    #                     help="Avoid using CUDA when available")
    parser.add_argument('--seed', type=int, default=42,
                        help="random seed for initialization")
    args = parser.parse_args()

    api = create_api() if not (args.app_key and args.app_secret and args.twitter_secret and args.twitter_key) else create_api(args.app_key,args.app_secret,args.twitter_secret,args.twitter_key)

    # this is test for posting tweets on my account
    # tweet_test = 'hello TWEET yo Tweet test '
    # api.update_status(status=tweet_test)
    #
    # print('check your twitter yo!')


    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    print('stream filter start, track terms:', settings.TRACK_TERMS)

    # 여기서 따로 p1 부르는걸 만들어 펑션을
    # stream_listener.use_multiprocess()
    stream.filter(track=settings.TRACK_TERMS) # blocking function. Runs until it finishes its task
    # async: use new thread to prevent disconnection to get the tweeet updates..




if __name__ == '__main__':
    main()
