import pandas as pd


df = pd.read_csv('final_prepped.csv')


# Count the occurrences of each class (0 and 1)
label_counts = df['engagement_label'].value_counts()

# Print the counts
print(label_counts)

# Check the proportion of each class
label_proportions = df['engagement_label'].value_counts(normalize=True)

# Print the proportions (as percentages)
print(label_proportions * 100)

