import random 
print("Welcome to the Rosy Bank..!")

create_acc = input("Do you want to create an account? (yes/no): ")

if create_acc == "yes":
    name = input("Enter your Name: ")
    acc_number = input("Enter your Account number: ")
    print("Hello",name,"Welcome to the Rosy Bank..!")
else:
    print("Thank you for visiting Rosy Bank..!")
    exit()


class bank:
    def __init__(self, acc_holder_name, balance, account_number=None):
        if account_number:
            self.acc_number = account_number
        else:
            self.acc_number = random.randint(1000, 9999)
        self.acc_holder_name = acc_holder_name
        self.balance = balance
        print("Your Account number is:", self.acc_number)

    def debit(self, amount):
        if amount > self.balance:
            print("Insufficient balance..!")
        else:
            self.balance -= amount
            print("Amount debited successfully..!")
            print("Your current balance is:", self.balance)

    def credit(self, amount):
        self.balance += amount
        print("Amount credited successfully..!")
        print("Your current balance is:", self.balance)

    def loan(self, amount):
        if amount > 100000:
            print("sorry..! poor guy not eligible for loan")
        else:
            print("Congratulations..! you are eligible for loan")


account1 = bank(name, 10000, acc_number)
account1.debit(2000)