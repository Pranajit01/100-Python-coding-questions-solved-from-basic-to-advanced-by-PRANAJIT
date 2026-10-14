"""Question 3: Basic Arithmetic Operations

Write a program to read two numbers and print their sum, difference, product and quotient.
"""

# Read the two numbers from standard input.
a = float(input())
b = float(input())

print("Sum:", a + b)
print("Difference:", a - b)
print("Product:", a * b)
if b == 0:
  print("Quotient: undefined (division by zero)")
else:
  print("Quotient:", a / b)