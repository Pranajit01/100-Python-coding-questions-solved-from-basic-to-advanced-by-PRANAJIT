"""Question 7: Swap Without a Third Variable

Write a program to swap two numbers without using a third variable.
"""

# Write your solution below.
a = int(input("Enter 1st No. : "))
b = int(input("Enter 2nd No.:"))
print(f"before swapping : {a},{b}")
a, b = b, a
print(f"after swapping: {a},{b}")