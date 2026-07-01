# Aggregate Calculation

ecat = float(input("Enter ECAT percentage: "))
inter = float(input("Enter Intermediate percentage: "))
matric = float(input("Enter Matric percentage: "))

aggregate = (ecat * 0.33) + (inter * 0.50) + (matric * 0.17)

print("Aggregate =", aggregate)