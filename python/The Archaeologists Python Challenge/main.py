import math

def calculate_age(carbon_14_ratio):
    # Half-life of Carbon-14 in years
    half_life = 5730

    # Decay constant
    decay_constant = math.log(2) / half_life

    # Initial Carbon-14 to Carbon-12 ratio (in ppt)
    initial_ratio = 1e-12

    # Calculate age using the decay formula
    age = - math.log(carbon_14_ratio) / decay_constant
    return age

# Input: Current Carbon-14 to Carbon-12 ratio
c14 = float(input("Enter the current Carbon-14 to Carbon-12 ratio in ppt: "))

# Output the result
print(f"The age of the artifact is approximately {calculate_age(c14):.2f} years.")