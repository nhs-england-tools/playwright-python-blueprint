class YesNoType:
    """
    Utility class for handling 'yes'/'no' type values.

    Members:
        YES: Represents a 'yes' value.
        NO: Represents a 'no' value.

    Methods:
        from_description(description: str) -> str:
            Returns the normalized 'yes' or 'no' value for a given description.
            Raises ValueError if the description is not recognized.
    """

    YES = "yes"
    NO = "no"

    _valid = {YES, NO}

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the normalized 'yes' or 'no' value for a given description.

        Args:
            description (str): The input description to normalize.

        Returns:
            str: 'yes' or 'no'.

        Raises:
            ValueError: If the description is not recognized as 'yes' or 'no'.
        """
        key = description.strip().lower()
        if key not in cls._valid:
            raise ValueError(f"Expected 'yes' or 'no', got: '{description}'")
        return key
