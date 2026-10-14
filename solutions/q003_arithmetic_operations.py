"""Question 3: Basic Arithmetic Operations

Write a program to read two numbers and print their sum, difference, product and quotient.
"""

# Write your solution below.

# Program to perform arithmetic operations on two numbers
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

# Arithmetic operations
print("Sum:", num1 + num2)
print("Difference:", num1 - num2)
print("Product:", num1 * num2)

if num2 != 0:
    print("Quotient:", num1 / num2)
else:
    print("Quotient: Cannot divide by zero")