list=[1,2,3,4,5,6,7,8,9]
squared_number = [x**2 for x in list if x%2 == 0]
print(squared_number)

list2=[1,2,3,4,5]
even_number = [x for x in list2 if x%2 ==0 ]
print(even_number)

list3= []
for i in range(1,100):
    if i %2 == 0:
        list3.append(i)
print(list3)

set1 = {1,2,2,2,3,4,4,4,5,5}
unique_num  = {x for x in set1}
print(unique_num)

key = {'a', 'b', 'c', 'd'}
value = {1,2,3,4}
user_dict = {k:b for k,b in zip(key,value)}
print("user_dictonary: ", user_dict)

