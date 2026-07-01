import math

x1 = float(input("Enter x1: "))
y1 = float(input("Enter y1: "))

x2 = float(input("Enter x2: "))
y2 = float(input("Enter y2: "))


def quadrant(x, y):
    if x > 0 and y > 0:
        return "Quadrant I"
    elif x < 0 and y > 0:
        return "Quadrant II"
    elif x < 0 and y < 0:
        return "Quadrant III"
    elif x > 0 and y < 0:
        return "Quadrant IV"
    elif x == 0 and y == 0:
        return "Origin"
    else:
        return "On Axis"


distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

print("Point 1:", quadrant(x1, y1))
print("Point 2:", quadrant(x2, y2))
print("Distance =", distance)