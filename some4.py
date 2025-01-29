class InvalidEmailException(Exception):
    pass

def validate_email(email):
    if '@' in email:
        return "Valid email"
    else:
        raise InvalidEmailException(f"Invalid email address: {email} please input @")


email = input("Enter email: ")

try:
    print(validate_email(email))
except InvalidEmailException as e:
    print(f"Error: {e}")
