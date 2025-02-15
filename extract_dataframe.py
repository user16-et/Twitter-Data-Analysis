import json
import pandas as pd
from textblob import TextBlob


def read_json(json_file: str) -> list:
    tweets_data = []
    for tweets in open(json_file, 'r'):
        tweets_data.append(json.loads(tweets))

    return len(tweets_data), tweets_data


class TweetDfExtractor:
    def __init__(self, tweets_list):
        self.tweets_list = tweets_list

    def find_statuses_count(self) -> list:
        statuses_count = []
        for tweet in self.tweets_list:
            statuses_count.append(tweet['user']['statuses_count'])
        return statuses_count

    def find_full_text(self) -> list:
        text = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys() and 'text' in tweet['retweeted_status'].keys():
                text.append(tweet['retweeted_status']['text'])
            else:
                text.append('Empty')
        return text

    def find_sentiments(self, text: list) -> list:
        polarity = []
        subjectivity = []
        for tweet in text:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        return polarity, subjectivity

    def find_created_time(self) -> list:
        created_at = []
        for time in self.tweets_list:
            created_at.append(time['created_at'])
        return created_at

    def find_source(self) -> list:
        source = []
        for x in self.tweets_list:
            source.append(x['source'])
        return source

    def find_screen_name(self) -> list:
        screen_name = []
        for x in self.tweets_list:
            screen_name.append(x['user']['screen_name'])
        return screen_name

    def find_followers_count(self) -> list:
        followers_count = []
        for x in self.tweets_list:
            followers_count.append(x['user']['followers_count'])
        return followers_count

    def find_friends_count(self) -> list:
        friends_count = []
        for x in self.tweets_list:
            friends_count.append(x['user']['friends_count'])
        return friends_count

    def is_sensitive(self) -> list:
        is_sensitive = []
        for tweet in self.tweets_list:
            if 'possibly_sensitive' in tweet.keys():
                is_sensitive.append(tweet['possibly_sensitive'])
            else:
                is_sensitive.append(None)
        return is_sensitive

    def find_favourite_count(self) -> list:
        favorite_count = []
        for tweet in self.tweets_list:
            if 'favourites_count' in tweet.keys():
                favorite_count.append(
                    tweet['favourites_count'])
            else:
                favorite_count.append(0)
        return favorite_count

    def find_retweet_count(self) -> list:
        retweet_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(
                    tweet['retweeted_status']['retweet_count'])
            else:
                retweet_count.append(0)
        return retweet_count

    def find_hashtags(self) -> list:
        hashtags = []
        for hs in self.tweets_list:
            hashtags.append(hs.get('entities', {}).get('hashtags', None))
        return hashtags

    def find_mentions(self) -> list:
        mentions = []
        for hs in self.tweets_list:
            mentions.append(", ".join(
                [mention['screen_name'] for mention in hs['entities']['user_mentions']]))
        return mentions

    def find_lang(self) -> list:
        lang = []
        for x in self.tweets_list:
            lang.append(x['user']['lang'])
        return lang

    def find_location(self) -> list:
        location = []
        for tweet in self.tweets_list:
            location.append(tweet['user']['location'])
        return location

    def get_tweet_df(self, save=True) -> pd.DataFrame:
        
        columns = ['created_at', 'source', 'original_text', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count,
                   screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('C:/Users/samuel/Desktop/10academy/Twitter-Data-Analysis/data/Economic_Twitter_Df.csv', index=False)
            print('Successfully Saved.')

        return df
if __name__ == "__main__":
    _, tweet_list = read_json("C:/Users/samuel/Desktop/10academy/Twitter-Data-Analysis/data/Economic_Twitter_Data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    df = tweet.get_tweet_df()
