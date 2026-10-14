"""Question 3: Basic Arithmetic Operations

Write a program to read two numbers and print their sum, difference, product and quotient.
"""

# Write your solution below.
first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))

print(f"Sum: {first_number + second_number}")
print(f"Difference: {first_number - second_number}")
print(f"Product: {first_number * second_number}")

if second_number == 0:
    print("Quotient: undefined (cannot divide by zero)")
else:
    print(f"Quotient: {first_number / second_number}")