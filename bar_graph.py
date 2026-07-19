import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
data = pd.read_csv("students.csv")

# Create Bar Graph
plt.bar(data["Name"], data["Marks"], color="green")

# Add Title and Labels
plt.title("Student Marks")
plt.xlabel("Student Name")
plt.ylabel("Marks")

# Display Graph
plt.show()