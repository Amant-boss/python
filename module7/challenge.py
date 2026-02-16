from selectors import SelectSelector

number1 = int(input("Enter the first number : "))
number2 = int(input("Enter the second number : "))
operator = input("Enter the operator : ")

if operator == "+":
    result = number1 + number2
elif operator == "-":
    result = number1 - number2
elif operator == "*":
    result = number1 * number2
elif operator == "/":
    result = number1 / number2
else:
    print("Error")
try:
    print(result)
except ZeroDivisionError:
    print("There is an error")