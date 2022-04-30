# Solution to IBM's Ponder This challenge from February 2022
# https://research.ibm.com/haifa/ponderthis/challenges/February2022.html
# Solved by Alexander Gramolin (https://github.com/gramolin/ponderthis)

from time import time
from math import ceil, gcd, log


def get_divisor_p3(number):
    """Find the largest power p3 such that 3^p3 divides the number."""
    max_p3 = ceil(log(number, 3))
    base_number = 3**max_p3
    gcd_value = gcd(number, base_number)
    return int(log(gcd_value, 3) + 1e-10)


def decompose(number, start_p2=None):
    """Decompose the number as a sum of coprime terms (2^p2)*(3^p3)."""
    decomposition = []
    p3 = get_divisor_p3(number)
    if start_p2 == None:
        p2 = int(log(number/(3**p3), 2) + 1e-10)
    else:
        p2 = start_p2
    while number > 0:
        new_number = number - (2**p2) * (3**p3)
        if new_number == 0:
            decomposition.append((p2, p3))
            return decomposition
        else:
            new_p3 = get_divisor_p3(new_number)
            if new_p3 > p3:
                decomposition.append((p2, p3))
                number = new_number
                p3 = new_p3
                p2 = int(log(number/(3**p3), 2) + 1e-10)
            else:
                p2 -= 1
    
    return None


def test_decomposition(number, decomposition):
    """Test if the decomposition of the number is correct."""
    summands = []
    for item in decomposition:
        summands.append((2**item[0]) * (3**item[1]))
    
    # Test if the decomposition is correct:
    correctness = (number == sum(summands))
    
    # Test that none of the summands divides another:
    divisibility = True
    for i in range(len(summands)-1):
        for j in range(i+1, len(summands)):
            if gcd(summands[i], summands[j]) == min(summands[i], summands[j]):
                divisibility = False
    
    # Length of the decomposition:
    length = len(decomposition)
    
    return correctness, divisibility, length


def solve(number):
    """Find a decomposition for the number and test it."""
    decomposition = decompose(number)
    print(number)
    print(decomposition)
    print("(correctness, divisibility, # of summands): "
          + str(test_decomposition(number, decomposition)) + "\n")


#####################################################################

# Start a timer:
start_time = time()

# Solution to the main problem:
print("*Solution for the number 10^199 with 122 summands:")
solve(number=10**199)

# Solution to the bonus problem:
print("*Solution for the number 10^299 with 186 summands:")
solve(number=10**299)

print("Done! It took {} seconds.".format(round(time() - start_time)))

