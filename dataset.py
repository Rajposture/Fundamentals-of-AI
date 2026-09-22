import pandas as pd

data = pd.read_csv("student_performance_dataset.csv")

print(data.head()) 
print(data.shape) #defines shape of that downloaded dataset 
print(data.info()) 