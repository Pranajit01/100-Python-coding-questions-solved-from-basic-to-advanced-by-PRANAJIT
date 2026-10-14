"""Question 5: Rectangle Area and Perimeter

Write a program to read the length and breadth of a rectangle and print its area and perimeter.
"""

# Write your solution below.
l = float(input("enter the length: "))
b = float(input("enter the breadth: "))
area = l * b
perimeter = 2 * (l + b)
print(f"Area: {area}\nPerimeter: {perimeter}")