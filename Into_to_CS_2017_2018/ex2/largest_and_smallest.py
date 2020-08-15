def largest_and_smallest(num1, num2, num3):
    """
    this function receives 3 numbers and returns a tuple 
    containing (the largest number, the smallest number)
    """
    min_num = num1
    max_num = num1

    # compares num2 to the min and max numbers
    # and sets the min and max numbers accordingly
    if num2 < min_num:
        min_num = num2
    else:
        max_num = num2

    # compares num3 to the min and max numbers
    # and sets the min and max numbers accordingly
    if num3 < min_num:
        min_num = num3
    elif num3 > max_num:
        max_num = num3

    return max_num, min_num
