# Find larger number using lambda function
# Then print its table using UDF

largest = lambda a, b: a if a > b else b

def print_table(num, rng):
    for i in range(1, rng + 1):
        print(f"{num} x {i} = {num * i}")

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

large_num = largest(a, b)

print("Larger Number =", large_num)

r = int(input("Enter range for table: "))

print_table(large_num, r)