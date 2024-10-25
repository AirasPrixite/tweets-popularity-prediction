import pandas as pd
from sklearn.utils import resample

df = pd.read_csv('final_prepped.csv')

# Assuming your dataset is in df and the engagement_label column indicates the class

# Separate majority and minority classes
df_majority = df[df['engagement_label'] == 0]
df_minority = df[df['engagement_label'] == 1]

# Undersample majority class
df_majority_undersampled = resample(df_majority,
                                    replace=False,    # sample without replacement
                                    n_samples=len(df_minority),  # match minority class size
                                    random_state=42)  # reproducibility

# Combine minority class with undersampled majority class
df_balanced = pd.concat([df_minority, df_majority_undersampled])

# Shuffle the resulting dataset
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

# Check the new class distribution
print(df_balanced['engagement_label'].value_counts())

df_balanced.to_csv('final_dataset.csv')


