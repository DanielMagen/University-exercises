def quadratic_equation(a, b, c):
    """
    this function receives 3 numbers representing the coefficients of 
    a quadratic equation
    it returns the solutions of the equation in a tuple of size 2
    if the equation has 1 solution or no solution the function will 
    set the second value of the tuple or both values of the tuple to 
    be None accordingly.
    """
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return None, None
    elif discriminant == 0:
        return -b / (2 * a), None

    discriminant = discriminant ** 0.5

    return (-b + discriminant) / (2 * a), (-b - discriminant) / (2 * a)


def quadratic_equation_user_input():
    """
    this function prompt the user to enter 3 numbers 
    it prints the number of solution a quadratic equation with 
    those 3 coefficients have, and if they have any prints them as well
    """
    a, b, c = input("insert coefficients a, b, and c:").split()
    a = float(a)
    b = float(b)
    c = float(c)

    solution1, solution2 = quadratic_equation(a, b, c)

    NO_SOLUTION = "The equation has no solutions"
    ONE_SOLUTION = "The equation has 1 solution"
    TWO_SOLUTIONS = "The equation has 2 solutions"

    if solution2 == None:
        if solution1 == None:
            print(NO_SOLUTION)
        else:
            print(ONE_SOLUTION, solution1)
    else:
        print(TWO_SOLUTIONS, solution1, "and", solution2)
