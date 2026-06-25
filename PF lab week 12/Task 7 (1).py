def detect_type(user_input):
    for t in [int, float]:
        try:
            t(user_input)
            if t == int:
                return "int"
            elif t == float:
                return "float"
        except ValueError:
            pass
    return "str"

value = input("Enter something: ")
print("Type:", detect_type(value))