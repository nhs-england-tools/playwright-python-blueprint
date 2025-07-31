class TemporaryAddressType:
    """
    Utility class for handling temporary address type values.

    Members:
        YES: Represents a 'yes' value.
        NO: Represents a 'no' value.
        EXPIRED: Represents an 'expired' value.
        CURRENT: Represents a 'current' value.
        FUTURE: Represents a 'future' value.

    Methods:
        from_description(description: str) -> str:
            Returns the normalized  value for a given description.
            Raises ValueError if the description is not recognized.
    """

    YES = "yes"
    NO = "no"
    EXPIRED = "expired"
    CURRENT = "current"
    FUTURE = "future"

    _valid = {YES, NO, EXPIRED, CURRENT, FUTURE}

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the normalized value for a given description.

        Args:
            description (str): The input description to normalize.

        Returns:
            str: 'yes', 'no', 'expired', 'current', 'future'.

        Raises:
            ValueError: If the description is not recognized as 'yes', 'no', 'expired', 'current', 'future'.
        """
        key = description.strip().lower()
        if key not in cls._valid:
            raise ValueError(f"Expected 'yes', 'no', 'expired', 'current', 'future', got: '{description}'")
        return key
