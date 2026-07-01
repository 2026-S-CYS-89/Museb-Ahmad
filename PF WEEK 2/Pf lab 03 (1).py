# Convert string to uppercase using lambda
# Reverse it using user defined function

uppercase = lambda s: s.upper()

def reverse_string(text):
    return text[::-1]

user_string = input("Enter a string: ")

upper_text = uppercase(user_string)

print("Uppercase String:", upper_text)
print("Reversed String:", reverse_string(upper_text))