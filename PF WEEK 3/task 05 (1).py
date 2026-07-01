import math

a = float(input("Enter a: "))
b = float(input("Enter b: "))
c = float(input("Enter c: "))

d = b**2 - 4*a*c

print("Discriminant =", d)

if d > 0:
    print("Roots are real and distinct")
    root1 = (-b + math.sqrt(d)) / (2*a)
    root2 = (-b - math.sqrt(d)) / (2*a)

elif d == 0:
    print("Roots are real and equal")
    root1 = root2 = -b / (2*a)

else:
    print("Roots are imaginary")
    real = -b / (2*a)
    imag = math.sqrt(-d) / (2*a)

    print(f"Root1 = {real} + {imag}i")
    print(f"Root2 = {real} - {imag}i")
    exit()

print("Root 1 =", root1)
print("Root 2 =", root2)