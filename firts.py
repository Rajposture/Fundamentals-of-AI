
import random
print("Enter the names of three Movies: ")
movie1 = input("Movie 1: ")
movie2 = input("Movie 2: ")
movie3 = input("Movie 3: ")

list = [movie1,movie2,movie3]
print(list)

print("Prediction must be done for the above movies: ")
for movie in list:
    print(f"- {movie}")

movie = random.choice(list)
print("Your favorite movie is: ",movie)



