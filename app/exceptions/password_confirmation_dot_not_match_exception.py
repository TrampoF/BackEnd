class PasswordConfirmationDotNotMatchException(Exception):
    """
    Raise when password and password confirmation do not match
    """

    def __init__(self):
        default_message = "Password and password confirmation do not match!"
        super().__init__(default_message)
