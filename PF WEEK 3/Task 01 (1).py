# Bytes to MB and GB

bytes_value = int(input("Enter bytes: "))

mb = bytes_value / (1024 ** 2)
gb = bytes_value / (1024 ** 3)

print("Mega Bytes =", mb)
print("Giga Bytes =", gb)