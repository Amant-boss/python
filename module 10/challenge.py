class DigitalSchool:
    def __init__(self, name, city, state, courses):
        self.__name = name
        self.__city = city
        self.__state = state
        self.__courses = courses

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def courses(self):
        return self.__courses

    @courses.setter
    def courses(self, courses):
        self.__courses = courses

    def show_school_info(self):
        print("Name : ", self.__name)
        print("City : ", self.__city)
        print("State : ", self.__state)
        print("Courses : ", self.__courses)

    def organize_hackathon(self):
        print("We are organizing a hackathon")

class Ds_Prishtina(DigitalSchool):
    def __init__(self, name, city, state, courses, student_number):
        super().__init__(name, city, state, courses)
        self._student_number = student_number

    @property
    def student_number(self):
        return self._student_number

    def SCF(self):
        print("Spring code fest is organized in Digital School")

    def organize_hackathon(self):
        print("Ds_prishtina is organizing a hackathon")

ds = Ds_Prishtina(
    name="Digital School",
    city="Prishtina",
    state="Kosova",
    courses="Coding courses", # Ensure this is lowercase to match __init__
    student_number=1724072304
)

print(f"The number of student in Ds_prishtina is {ds.student_number}")