LOWER = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
UPPER = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
NUMS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
SPECIAL = ('!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', '|','\\', ';', ':', "'", '"', ',', '<', '.', '>', '/', '?', '`', '~')

def generate_password(length: int = 8, include_lower: bool = True, include_upper: bool = True, include_nums: bool = True, include_special: bool = True) -> str:
    if (length < 4):
        raise ValueError("Password length must be at least 4.")
    if not (include_lower or include_upper or include_nums or include_special):
        raise ValueError("At least one character type must be included.")
    
    import random
    password = []

    characters = []
    if include_lower:
        characters.extend(LOWER)
        password.append(random.choice(LOWER))
    if include_upper:
        characters.extend(UPPER)
        password.append(random.choice(UPPER))
    if include_nums:
        characters.extend(NUMS)
        password.append(random.choice(NUMS))
    if include_special:
        characters.extend(SPECIAL)
        password.append(random.choice(SPECIAL))

    while len(password) < length:
        password.append(random.choice(characters))
    
    random.shuffle(password)
    password = ''.join(password)

    return password