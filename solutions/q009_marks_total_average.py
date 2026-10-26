"""Question 9: Marks Total and Average

Write a program to read the marks of 5 subjects and print the total and average.
"""

# Write your solution below.
mark1 = float(input("Enter the marks for subject 1: "))
mark2 = float(input("Enter the marks for subject 2: "))
mark3 = float(input("Enter the marks for subject 3: "))
mark4 = float(input("Enter the marks for subject 4: "))
mark5 = float(input("Enter the marks for subject 5: "))

total = mark1 + mark2 + mark3 + mark4 + mark5
average = total / 5

print(f"Total marks: {total}")
print(f"Average marks: {average}")
