import numpy as np

try:
    N = int(input("How many different objects are there (numbers, birthdays, etc.)? "))
    k = int(input("How many objects are you drawing? "))
except:
    raise ValueError("Please provide appropriate values (positive integers).")

probln = 0
if k>N:
    prob = 100
else:
    for i in range(k):
        probln += np.log(N-i) - np.log(N)
    prob = 100 - 100 * np.exp(probln)

print(f"There is a {prob:.2f}% chance that you will draw at least two of the same object.")
