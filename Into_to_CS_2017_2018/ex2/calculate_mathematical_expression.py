def calculate_mathematical_expression(num1, num2, operation):
    """
    this function receives 2 numbers and an operation that is either 
    "+","-","/","*"
    returns the mathematical value of the operation applied to those numbers
    """
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            return None
        return num1 / num2
    else:
        return None


def calculate_from_string(text):
    """
    this function receives a text that contains
    a mathematical expression, and returns its result
    """
    num1, operation, num2 = text.split()
    num1 = float(num1)
    num2 = float(num2)
    return calculate_mathematical_expression(num1, num2, operation)
