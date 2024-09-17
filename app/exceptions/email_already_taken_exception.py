class EmailAlreadyTakenException(Exception):
    """
    Raise when email is already taken by another user
    """

    def __init__(self):
        default_message = "This email is already taken"
        super().__init__(default_message)
