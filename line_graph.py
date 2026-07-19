import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
data = pd.read_csv("students.csv")

# Create line graph
plt.plot(data["Name"], data["Marks"], marker='o', linestyle='-', color='blue')

# Add title and labels
plt.title("Student Marks")
plt.xlabel("Student Name")
plt.ylabel("Marks")

# Display grid
plt.grid(True)

plt.show()