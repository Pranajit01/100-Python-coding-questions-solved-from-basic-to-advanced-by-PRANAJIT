"""Question 4: Circle Area and Circumference

Write a program to read the radius of a circle and print its area and circumference.
"""

import math

# Write your solution below.
radius = float(input("Enter radius: "))
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius
print("The area of the circle is:", area)
print("The circumference of the circle is:", circumference)