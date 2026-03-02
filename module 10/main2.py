class Student:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

student1 = Student("Amant", 13)

print("Name : " , student1.name)
print("Age : " , student1.age)

student1.name = "Deon"
student1.age = 16

print("Name : " , student1.name)
print("Age : " , student1.age)