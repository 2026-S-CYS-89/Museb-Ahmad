

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

def permutation(n, r):
    return factorial(n) // factorial(n - r)

def combination(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

n = int(input("Enter value of n: "))
r = int(input("Enter value of r: "))

print("Permutation =", permutation(n, r))
print("Combination =", combination(n, r))

