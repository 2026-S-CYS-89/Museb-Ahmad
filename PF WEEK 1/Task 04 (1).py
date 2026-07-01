# Random Password Generator

import random
import string

length = int(input("Enter password length: "))

password = ""

uppercase = input("Include uppercase letters? (y/n): ")
lowercase = input("Include lowercase letters? (y/n): ")
digits = input("Include digits? (y/n): ")
special = input("Include special characters? (y/n): ")

characters = ""

if uppercase == 'y':
    characters += string.ascii_uppercase

if lowercase == 'y':
    characters += string.ascii_lowercase

if digits == 'y':
    characters += string.digits

if special == 'y':
    characters += string.punctuation

if characters == "":
    print("No character type selected!")

else:
    for i in range(length):
        password += random.choice(characters)

    print("Generated Password =", password)