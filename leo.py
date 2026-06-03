
import exp
exp.greet("Raj")
print("This is my new line added to file.")
file = open("llm.txt","w")
file.write("this is my first line in llm")
file.close()
file = open("llm.txt","r")
file.content = file.read()
print(file.content)
file.close()