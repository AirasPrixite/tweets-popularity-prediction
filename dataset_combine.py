import pandas as pd

# Initialize an empty DataFrame
df_popularity = pd.DataFrame()

# Read the CSV files
df_new = pd.read_csv('tweets.csv')
df_old = pd.read_csv('analyze.csv')
df_chatgpt = pd.read_csv('Twitter Jan Mar.csv')

# Select and append relevant columns from each DataFrame
df_popularity = pd.concat([
    pd.DataFrame({
        'tweet_text': df_new['content'],
        'like_count': df_new['number_of_likes'],
        'retweet_count': df_new['number_of_shares']
    }),
    pd.DataFrame({
        'tweet_text': df_old['text'],
        'like_count': df_old['like_count'],
        'retweet_count': df_old['retweet_count']
    }),
    pd.DataFrame({
        'tweet_text': df_chatgpt['content'],
        'like_count': df_chatgpt['retweet_count'],  # Correcting the swapped columns
        'retweet_count': df_chatgpt['like_count']
    })
], ignore_index=True)  # This ensures rows are appended without index conflicts

# Save the combined DataFrame to a CSV file
df_popularity.to_csv('final.csv', index=False)

# Print the combined DataFrame
print(df_popularity)
