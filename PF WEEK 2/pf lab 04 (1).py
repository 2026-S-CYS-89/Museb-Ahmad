# Temperature Converter using User Defined Functions

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

choice = int(input("1. Celsius to Fahrenheit\n2. Fahrenheit to Celsius\nEnter choice: "))

if choice == 1:
    c = float(input("Enter temperature in Celsius: "))
    print("Temperature in Fahrenheit =", celsius_to_fahrenheit(c))

elif choice == 2:
    f = float(input("Enter temperature in Fahrenheit: "))
    print("Temperature in Celsius =", fahrenheit_to_celsius(f))

else:
    print("Invalid Choice")