import random
print("Welcome to the Guessing Game..!")
number = random.randint(1,100)

guess = int(input("Enter your guess: "))
while True:
    if guess < number:
        print("Too low..! Try again.")
        guess = int(input("Enter your guess: "))
    elif guess > number:
            print("Too high..! Try again.")
            guess = int(input("Enter your guess: "))
    else:
                print("Congratulations..! You guessed the number correctly.")
                break
    print("The number was: ",number)
    print("Better luck next time..!")
    