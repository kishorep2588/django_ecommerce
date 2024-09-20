import time

while True:
    num1 = input('Enter the Number: ')
    num2 = input('Enter the Number2: ')
    operation = input('Enter the Operation: ')
    if operation == '+':
        print(int(num1) + int(num2))
    elif operation == '-':
        print(int(num1) - int(num2))
    elif operation == '*':
        print(int(num1) * int(num2))
    elif operation == '/':
        print(int(num1) / int(num2))
    elif operation == '%':
        print(int(num1) % int(num2))
    elif operation == '**':
        print(int(num1) ** int(num2))
    
