print("The user data is going to store in a dictionary")
user_data = {}
print("Enter the number of data you want to store: ")
n = int(input())
for i in range(n):
    key = input("Enter the key: ")
    value = input("Enter the value: ")
    user_data[key] = value
print("The user data is: ",user_data)