import pandas as pd

# Read CSV file
data = pd.read_csv("students.csv")

# Display first 5 records
print("First 5 Records:")
print(data.head())

# Display last 5 records
print("\nLast 5 Records:")
print(data.tail())

# Display dataset information
print("\nDataset Information:")
data.info()

# Display statistical summary
print("\nStatistical Summary:")
print(data.describe())

# Display column names
print("\nColumn Names:")
print(data.columns)

# Display dataset dimensions
print("\nShape of Dataset:")
print(data.shape)