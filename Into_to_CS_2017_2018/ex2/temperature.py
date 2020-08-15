def is_it_summer_yet(temperature_threshold, masurement1, masurement2, masurement3):
    """
    this function receives 4 numbers representing 
    a temperature threshold
    and 3 temperature measurements
    
    if 2 of those measurements or more are higher than
    the given temperature threshold it returns True
    and False otherwise 
    """
    if temperature_threshold < masurement1:
        if temperature_threshold < masurement2:
            return True
        elif temperature_threshold < masurement3:
            return True

    elif temperature_threshold < masurement2:
        if temperature_threshold < masurement3:
            return True

    return False
