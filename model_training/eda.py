import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('final_dataset.csv')
# Display the first few rows
print(df.head())
# Check the shape of the dataset
print(f'Dataset Shape: {df.shape}')
# Get data types and missing values
print(df.info())
# Get summary statistics
print(df.describe())
# Count plot for engagement label
plt.figure(figsize=(8, 5))
sns.countplot(x='engagement_label', data=df)
plt.title('Distribution of Engagement Label')
plt.xlabel('Engagement Label')
plt.ylabel('Count')
plt.xticks(ticks=[0, 1], labels=['Low Engagement', 'High Engagement'])
plt.show()
# Calculate the correlation matrix
# Exclude non-numeric columns for correlation
numeric_df = df.select_dtypes(include='number')

# Calculate the correlation matrix
corr = numeric_df.corr()

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Draw the heatmap
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Matrix')
plt.show()

# Set the style
sns.set(style="whitegrid")

# Plotting numerical features
num_features = ['like_count', 'retweet_count', 'tweet_length', 'engagement_score']

plt.figure(figsize=(15, 10))
for i, feature in enumerate(num_features):
    plt.subplot(2, 2, i + 1)
    sns.histplot(df[feature], bins=30, kde=True)
    plt.title(f'Distribution of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
# Count plots for categorical features
categorical_features = ['has_mention', 'has_hashtag', 'has_emojis', 'has_url', 'tweet_sentiment']

plt.figure(figsize=(15, 10))
for i, feature in enumerate(categorical_features):
    plt.subplot(2, 3, i + 1)
    sns.countplot(x=feature, hue='engagement_label', data=df)
    plt.title(f'{feature} vs Engagement Label')
    plt.xlabel(feature)
    plt.ylabel('Count')

plt.tight_layout()
plt.show()
