"""Question 12: Positive, Negative, or Zero

Write a program to read a number and check whether it is positive, negative or zero.
"""

# Write your solution below.
number = float(input("Enter a number: "))

if number > 0:
    print("Positive Number")
elif number < 0:
    print("Negative Number")
else:
    print("Zero")
