


import re


def is_password_safe(password: str) -> bool:
    """
    Check if the password is safe according to certain criteria.
    :param password: The password to check.
    :return: True if the password is safe, False otherwise.
    """
    pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" 
    if not re.match(pattern, password):
        return False
    
    return True