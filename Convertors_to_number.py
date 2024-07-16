# conver views into number
def convert_suffix_to_number(suffix_string):
    suffix_string = suffix_string.lower()
    multipliers = {'k': 1000, 'm': 1000000}

    if suffix_string[-1] in multipliers:
        multiplier = multipliers[suffix_string[-1]]
        return int(float(suffix_string[:-1]) * multiplier)
    else:
        return int(float(suffix_string))
    
