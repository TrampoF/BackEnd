class InvalidEmailFormatException(Exception):
    """
    Raise when email have a wrong fortmat
    """

    def __init__(self):
        default_message = "Invalid email format"
        super().__init__(default_message)
