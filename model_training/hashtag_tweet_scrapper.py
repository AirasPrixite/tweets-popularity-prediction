import requests
import pandas as pd

BEARER_TOKEN = None

def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers

def get_user_tweets(username, max_results=100):
    headers = create_headers(BEARER_TOKEN)
    url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{username}&tweet.fields=public_metrics,entities&max_results={max_results}"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    
    tweets = response.json().get('data', [])
    return tweets

def get_tweets_by_hashtag(hashtag, max_results=100):
    headers = create_headers(BEARER_TOKEN)
    
    if hashtag.startswith('#'):
        hashtag = hashtag[1:]
    
    url = f"https://api.twitter.com/2/tweets/search/recent?query={hashtag}&tweet.fields=public_metrics,entities&max_results={max_results}"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}, Response: {response.text}")
    
    tweets = response.json().get('data', [])
    return tweets

def extract_tweet_data(tweets):
    tweet_data = []
    for tweet in tweets:
        tweet_text = tweet.get('text')
        public_metrics = tweet.get('public_metrics', {})
        hashtags = tweet.get('entities', {}).get('hashtags', [])
        mentions = tweet.get('entities', {}).get('mentions', [])
        tweet_data.append([
            tweet_text,
            public_metrics.get('like_count', 0),
            public_metrics.get('retweet_count', 0),
            public_metrics.get('reply_count', 0),
            len(hashtags) > 0,
            len(hashtags),
            len(mentions) > 0,
            len(tweet_text),
            public_metrics.get('quote_count', 0)
        ])
    return tweet_data

def collect_and_save_tweets(accounts, hashtags, max_results=100):
    all_tweet_data = []
    
    for account in accounts:
        tweets = get_user_tweets(account, max_results=max_results)
        tweet_data = extract_tweet_data(tweets)
        all_tweet_data.extend(tweet_data)
    
    for hashtag in hashtags:
        tweets = get_tweets_by_hashtag(hashtag, max_results=max_results)
        tweet_data = extract_tweet_data(tweets)
        all_tweet_data.extend(tweet_data)
    
    df = pd.DataFrame(all_tweet_data, columns=['Tweet_text', 'Likes_count', 'Retweet_count', 'Reply_count', 
                                               'Has_hashtag', 'no_of_hashtags', 'Has_mention', 
                                               'Tweet_length', 'quote_count'])
    df.to_csv('tweets_dataset_4.csv', index=False)
    print("Tweets data saved to 'tweets_dataset.csv'")

accounts = []
hashtags = ['#31DaysofHorror', '#Now Watching']
collect_and_save_tweets(accounts, hashtags, max_results=100)
