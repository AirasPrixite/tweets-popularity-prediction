import tweepy
import csv
import time

bearer_token = None
client = tweepy.Client(bearer_token=bearer_token)

def fetch_detailed_tweets_v2(username, count=100):
    user = client.get_user(username=username)
    user_id = user.data.id

    tweets = client.get_users_tweets(id=user_id, max_results=count, tweet_fields=['created_at', 'lang', 'source', 'public_metrics'])

    detailed_tweets = []
    for tweet in tweets.data:
        metrics = tweet.public_metrics
        tweet_data = {
            'text': tweet.text,
            'created_at': tweet.created_at,
            'lang': tweet.lang,
            'source': tweet.source,
            'retweet_count': metrics['retweet_count'],
            'like_count': metrics['like_count'],
            'reply_count': metrics['reply_count'],
            'quote_count': metrics['quote_count']
        }
        detailed_tweets.append(tweet_data)

    return detailed_tweets

def save_to_csv(tweets, filename='tweets.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['text', 'created_at', 'lang', 'source', 'retweet_count', 'like_count', 'reply_count', 'quote_count'])
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet)

username = "GiveawayBandit"
detailed_tweets = fetch_detailed_tweets_v2(username)

save_to_csv(detailed_tweets, 'giveaway_bandit_tweets.csv')
print(f"Scraped {len(detailed_tweets)} tweets and saved them to 'giveaway_bandit_tweets.csv'.")
