try :
    result = 10/0
except ZeroDivisionError:
    print("There is an error")

fruits = {
    "apple": 5,
    "banana": 7,
    "orange": 3
}

try:
    print(fruits["cherry"])
except KeyError:
    print("That doesnt exist")