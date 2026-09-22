import pandas as pd

data = {
    "Name": ["Raj", "Amit", "Neha", "Riya"],
    "Marks": [80, 65, 90, 75]
}

df = pd.DataFrame(data)

print("Student Data:")
print(df)

print("\nFirst rows:")
print(df.head())

print("\nInformation:")
df.info()

print("\nStatistics:")
print(df.describe())

print("\nSorted Marks:")
print(df.sort_values("Marks"))