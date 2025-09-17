from typing import Optional


class SelectionBuilderException(Exception):
    """
    Exception used for subject selection errors in the selection builder.

    This exception is raised when an invalid or unexpected value is encountered
    during subject selection logic.
    """

    def __init__(self, message_or_key: str, value: Optional[str] = None):
        """
        Initialize a SelectionBuilderException.

        Args:
            message_or_key (str): The error message or the key for which the error occurred.
            value (Optional[str]): The invalid value, if applicable.
        """
        if value is None:
            message = message_or_key
        else:
            message = f"Invalid '{message_or_key}' value: '{value}'"
        super().__init__(message)
