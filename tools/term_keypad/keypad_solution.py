#!/usr/bin/env python3

import collections
import itertools
import math

def is_prime(num):
    # Is it even?
    if num % 2 == 0:
        return False

    # Check odd divisors from 3 to the square root of the number
    for divisor in range(3, int(math.sqrt(num)) + 1, 2):
        if num % divisor == 0:
            return False

    return True
    

# We start with our keys
warm_keys = ["1", "3", "7"]

for option in itertools.product(warm_keys, repeat=4):
    # Remove anything where the most common element appears more than twice
    most_common, count = collections.Counter(option).most_common(1)[0]
    if count > 2:
        continue

    # Convert to int
    num = int("".join(option))

    if is_prime(num):
        print(num)
