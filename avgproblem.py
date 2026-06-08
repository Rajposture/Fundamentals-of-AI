class report:
    def __init__(self,name,marks):
        self.name = name
        self.marks = marks
    def avg (self):
        return sum(self.marks)/len(self.marks)
    def grade(self):
        average = self.avg()
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    def __sub__(self, subjects):
        self.subjects  = subjects
        return self.subjects
    def __percentage__(self):
        sum = 0
        for marks in self.marks:
            sum  += marks
            return sum/len(self.marks)
        


student1 = report("Raj", [80, 90, 85])
print("Name:", student1.name)
print("Marks:", student1.marks)
print("Average Marks:", student1.avg())
print("Grade:", student1.grade())
subjects = student1 - ["Math", "Science", "English"]
print("Subjects:", subjects)
print("Percentage: ", student1.__percentage__())

