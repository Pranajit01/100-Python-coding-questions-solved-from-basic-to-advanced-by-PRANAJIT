"""Question 10: Convert Seconds

Write a program to read seconds and convert them into hours, minutes and seconds.
"""

# Write your solution below.
total_seconds = int(input("Enter the total number of seconds: "))
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
remaining_seconds = total_seconds % 60

print(
    f"Hours: {hours}, Minutes: {minutes}, "
    f"Seconds: {remaining_seconds}"
)