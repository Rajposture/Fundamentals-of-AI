print("Welcome to the Time Table mchine..! ")
print("According to 24 Hrs Clock.")
time = int(input("Enter Your Time: "))
if time in range (1,6):
    print("Sleeping time..")
elif time in range (7,8):
    print("Bath time..")
elif 9 <= time <= 10:
    print("Breakfast time..")
elif time in range(11,12):
    print("study time..")
elif time in range (12 ,17):
    print("school time..")
elif time in range(18,19):
    print("Playing time..")
elif time in range (19,20):
    print("Home work Time.")
elif time in range(21,22):
    print("Dinner time.")
else :
    print("sleeping time.")
