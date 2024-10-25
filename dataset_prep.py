import pandas as pd
import re
from textblob import TextBlob
from tqdm import tqdm

# Read the CSV file
df = pd.read_csv('final.csv')

# Drop rows where tweet_text is NaN
df = df.dropna(subset=['tweet_text'])

# Enable tqdm for pandas apply
tqdm.pandas()

# Function to handle sentiment analysis
def get_sentiment(tweet):
    blob = TextBlob(tweet)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return 2  # Positive
    elif sentiment_score < 0:
        return 0  # Negative
    else:
        return 1  # Neutral

# Function to check if tweet has a mention (@)
def has_mention(text): 
    mention_pattern = r'@\w+'
    if re.search(mention_pattern, text):
        return 1  # Mention present
    return 0  # No mention

# Function to check if tweet has hashtags (#)
def has_hashtags(tweet: str) -> int:
    hashtag_pattern = r'#\w+'
    if re.search(hashtag_pattern, tweet):
        return 1  # Has hashtag
    return 0  # No hashtag

# Function to check if tweet contains emojis
def has_emojis(tweet):
    emoji_pattern = re.compile(
        r'['
        r'\U0001F600-\U0001F64F'  # emoticons
        r'\U0001F300-\U0001F5FF'  # symbols & pictographs
        r'\U0001F680-\U0001F6FF'  # transport & map symbols
        r'\U0001F700-\U0001F77F'  # alchemical symbols
        r'\U0001F780-\U0001F7FF'  # Geometric Shapes Extended
        r'\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
        r'\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
        r'\U0001FA00-\U0001FA6F'  # Chess Symbols
        r'\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
        r'\U00002700-\U000027BF'  # Dingbats
        r'\U0001F1E0-\U0001F1FF'  # Flags (iOS)
        r']+', flags=re.UNICODE)
    if emoji_pattern.search(tweet):
        return 1  # Contains emoji
    return 0  # No emoji

# Function to check if tweet contains a URL
def has_url(tweet):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')    
    if url_pattern.search(tweet):
        
        return 1  # Has URL
    return 0  # No URL

# Apply the functions with progress bars using tqdm
df['like_count_normalized'] = df['like_count'] / df['like_count'].max()
df['retweet_count_normalized'] = df['retweet_count'] / df['retweet_count'].max()

df['engagement_score'] = (
    1 * df['like_count_normalized'] +
    2 * df['retweet_count_normalized']
)

df['has_mention'] = df['tweet_text'].progress_apply(has_mention)
df['has_hashtag'] = df['tweet_text'].progress_apply(has_hashtags)
df['tweet_sentiment'] = df['tweet_text'].progress_apply(get_sentiment)
df['has_emojis'] = df['tweet_text'].progress_apply(has_emojis)
df['tweet_length'] = df['tweet_text'].progress_apply(len)  # Directly use len() for tweet length
df['has_url'] = df['tweet_text'].progress_apply(has_url)
threshold = df['engagement_score'].quantile(0.80)  # Top 20% of tweets as high engagement
df['engagement_label'] = (df['engagement_score'] > threshold).astype(int)

# Print the updated DataFrame
print(df)

df.to_csv('final_prepped.csv')



