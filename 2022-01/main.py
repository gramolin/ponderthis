# Solution to IBM's Ponder This challenge from January 2022
# https://research.ibm.com/haifa/ponderthis/challenges/January2022.html
# Solved by Alexander Gramolin (https://github.com/gramolin/ponderthis)

from time import time
from sympy import isprime


def generate_primes(d):
    """Generate a set of all primes with d distinct digits."""
    primes = set()
    for i in range(10**(d-1)+1, 10**d, 2):
        string = str(i)
        unique_string = "".join(set(string))
        if len(string) == len(unique_string): # Check that all digits are unique
            if isprime(i): # Check that the number is prime
                primes.add(str(i))
    return primes


def reorder_circle(circle):
    """Reorder the circle elements so that it starts from the lowest element
        and goes to the direction of the smallest of two possible second elements.
        For example, the circle "4736201" becomes "0147362". The circle
        "32187654" becomes "12345678"."""
    length = len(circle)
    assert length == len(set(circle)), "Not all elements of the circle are unique!"
    digits = [int(i) for i in list(circle)] 
    new_circle = str(min(digits))
    start_index = circle.find(new_circle)
    neighbors = [circle[start_index-1], circle[(start_index+1) % length]]
    if int(neighbors[0]) > int(neighbors[1]):
        new_circle += circle[start_index+1:]
        new_circle += circle[:start_index]
    else:
        new_circle += circle[:start_index][::-1] # Reverse direction
        new_circle += circle[start_index+1:][::-1] # Reverse direction
    assert len(new_circle) == len(circle), "Wrong length of the new circle!"
    assert set(new_circle) == set(circle), "Wrong elements in the new circle!"
    return new_circle


def generate_all_circles(length, circles=[""]):
    """Recursively generate a set of all circles with given length."""
    assert length < 11, "The lengths is too big!"
    if len(circles[0]) == length:
        return circles
    else:
        new_circles = []
        for circle in circles:
            digits = set("0123456789").difference(set(circle))
            for digit in digits:
                new_circles.append(circle + digit)
        return generate_all_circles(length, new_circles)


def clean_circle_list(circle_list):
    """Clean up the list of circles by removing duplicate circles."""
    circle_set = set()
    for circle in circle_list:
        circle_set.add(reorder_circle(circle))
    return list(circle_set)


def get_single_score(circle, prime):
    """Calculate the score given the circle and the prime number (both are strings)."""
    score = 0
    circle_length = len(circle)
    for i in range(len(prime)-1):
        position = circle.find(prime[i])
        step = abs(position - circle.find(prime[i+1]))
        score += min(step, circle_length-step)
    return score


def get_scores(circles, primes):
    """Calculate the total scores given the list of circles and the list of primes."""
    length = len(circles[0])
    scores = []
    for circle in circles:
        circle_set = set(circle)
        score = 0
        for prime in primes:
            prime_set = set(prime)
            if prime_set.issubset(circle_set):
                score += get_single_score(circle, prime)
        scores.append(score)
    return scores


def solve(n, d):
    """Get solutions for the (n, d) case."""
    print("Solution for the case n = {}, d = {}:".format(n, d))
    p = generate_primes(d) # List of primes with d distinct digits
    c = clean_circle_list(generate_all_circles(n)) # List of circles with n distinct digits
    
    # Calculate the total score for each circle:
    scores = get_scores(circles=c, primes=p)
    
    # Find the minimum and maximum scores:
    min_score = min(scores)
    max_score = max(scores)
    
    # Find indices corresponding to the minimum and maximum scores:
    min_indices = [i for i, v in enumerate(scores) if v == min_score]
    max_indices = [i for i, v in enumerate(scores) if v == max_score]
    
    # Print out solutions with the minimum score:
    print("*Circles with the minimum score of {} (up to permutations):".format(min_score))
    for index in min_indices:
        ans = [int(i) for i in list(c[index])]
        print(ans)
    
    # Print out solutions with the maximum score:
    print("*Circles with the maximum score of {} (up to permutations):".format(max_score))
    for index in max_indices:
        ans = [int(i) for i in list(c[index])]
        print(ans)
    print("") # Empty line


#####################################################################

# Start a timer:
start_time = time()

# Solution to the main problem:
solve(n=7, d=5)

# Solution to the bonus problem:
solve(n=8, d=6)

print("Done! It took {} seconds.".format(round(time() - start_time)))

