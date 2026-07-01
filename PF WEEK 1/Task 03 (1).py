# Display prime numbers in a range and their sum

start = int(input("Enter starting range: "))
end = int(input("Enter ending range: "))

sum_prime = 0

print("Prime Numbers:")

for num in range(start, end + 1):
    if num > 1:
        is_prime = True

        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break

        if is_prime:
            print(num)
            sum_prime += num

print("Sum of Prime Numbers =", sum_prime)