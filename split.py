import pandas as pd
from sklearn.model_selection import train_test_split

# Load the Housing dataset
data = pd.read_csv("Housing.csv")

# Display dataset size
print("Original dataset shape:", data.shape)

# Split dataset into training and testing data
train_data, test_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

# Display the sizes
print("Training data shape:", train_data.shape)
print("Testing data shape:", test_data.shape)

# Save the datasets
train_data.to_csv("train.csv", index=False)
test_data.to_csv("test.csv", index=False)