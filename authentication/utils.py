


def is_password_safe(password: str) -> bool:
    """
    Check if the password is safe according to certain criteria.
    :param password: The password to check.
    :return: True if the password is safe, False otherwise.
    """
    # Example criteria: at least 8 characters, contains both letters and numbers
    if len(password) < 8:
        return False
    
    # Check if the password contains at least one number
    if not any(char.isdigit() for char in password):
        return False
    
    # Check if the password contains at least one letter and not only digits
    if not any(char.isalpha() for char in password):
        return False

    # Check if the password contains at least one special character
    if password.isalnum():
        return False
    
    return True