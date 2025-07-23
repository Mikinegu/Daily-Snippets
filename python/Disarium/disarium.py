def is_disarium(number):
    digits = [int(d) for d in str(number)]
    total = sum(digit ** (index + 1) for index, digit in enumerate(digits))
    return total == number

# Example usage
num = int(input("Enter a number: "))
if is_disarium(num):
    print(f"{num} is a Disarium number.")
else:
    print(f"{num} is not a Disarium number.")
