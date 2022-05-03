# Solution to IBM's Ponder This challenge from March 2022
# https://research.ibm.com/haifa/ponderthis/challenges/March2022.html
# Solved by Alexander Gramolin (https://github.com/gramolin/ponderthis)

from time import time
from sympy import isprime


def generate_primes(length):
    """Generate a list of all primes of given length."""
    primes = []
    for i in range(10**(length-1)+1, 10**length, 2):
        if isprime(i): # Check that the number is prime
            primes.append(str(i))
    return primes


def generate_all_masks(length, masks=[""]):
    """Recursively generate a list of all possible masks of given length.
    Masks consist of the following symbols (similar to the Wordle game):
    0 -- green tile (correct digit and correct position);
    1 -- yellow tile (correct digit but wrong position);
    2 -- gray tile (wrong digit)."""
    if len(masks[0]) == length:
        return masks
    else:
        new_masks = []
        for mask in masks:
            new_masks.extend([mask+"2", mask+"1", mask+"0"])
        return generate_all_masks(length, new_masks)


def generate_template(guess, mask):
    """Given a guess and a mask, generate the template.
    This is a list, each element of which is a set of possible
    digits for the corresponding position. For example,
    if template[3] = {"1", "3"} then the fourth digit is 1 or 3."""
    length = len(guess)
    template = []
    required_digits = set() # Set of digits that must be present
    excluded_digits = set() # Set of digits that are excluded
    
    for i in range(length):
        template.append(set())
        if mask[i] == "0": # Green tile
            template[i].add(guess[i])
        elif mask[i] == "1": # Yellow tile
            required_digits.add(guess[i])
        elif mask[i] == "2": # Gray tile
            excluded_digits.add(guess[i])
    
    possible_digits = set("0123456789").difference(excluded_digits)
    
    for i in range(length):
        if mask[i] == "1": # Yellow tile
            template[i] = possible_digits.difference(guess[i])
        elif mask[i] == "2": # Gray tile
            template[i] = possible_digits
    
    # The first digit cannot be "0":
    template[0] = template[0].difference({"0"})
    
    # The last digit cannot be even or "5" (the number should be prime):
    template[-1] = template[-1].difference(set("024568"))
    
    return template, required_digits


def count_remaining_solutions(guess, mask, primes):
    """Given a guess and a mask, count all possible solutions."""
    template, required_digits = generate_template(guess, mask)
    
    solutions = [""]
    
    # Generate all solutions following the template:
    for i in range(len(guess)):
        new_solutions = []
        for solution in solutions:
            for digit in template[i]:
                new_solutions.append(solution + digit)
        solutions = new_solutions
    
    # Only the prime solutions are valid:
    solutions = set(solutions).intersection(primes)
    
    count = 0
    for solution in solutions:
        # Check that all the required digits are present:
        if required_digits.issubset(set(solution)):
            count += 1
    
    return count


def get_score(guess, masks, primes, max_score):
    """Find the score for a specific guess.
    Stop if the score is larger than max_score."""
    score = 0
    for mask in masks:
        score += count_remaining_solutions(guess, mask, primes)**2
        if score > max_score:
            break
    return score


def find_best_guess(guesses, masks, primes):
    """Find the guess giving the lowest score."""
    best_score = 1e10
    for guess in guesses:
        score = get_score(guess, masks, primes, best_score)
        if score <= best_score:
            best_score = score
            best_guess = guess
    return best_guess, best_score


def solve(n):
    """Solve the problem for a specific length n."""
    primes = generate_primes(n)
    masks = generate_all_masks(n)
    
    best_guess, best_score = find_best_guess(primes, masks, set(primes))
    
    print("Case n = {}: p = {}, E[p] = {}/{}\n".format(n, best_guess, best_score, len(primes)))


#####################################################################

# Start a timer:
start_time = time()

# Solution to the main problem:
solve(n=5)

print("Done! It took {} seconds.".format(round(time() - start_time)))

