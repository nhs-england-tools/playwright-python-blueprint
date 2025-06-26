class InvitedSinceAgeExtension:
    """
    Utility class for mapping subject invitation criteria based on age extension presence.

    This class provides:
        - Logical flags for "yes" and "no" to indicate if a subject was invited since the age extension.
        - A method to convert a description to a valid flag.

    Methods:
        from_description(description: str) -> str:
            Returns the logical flag ("yes" or "no") for a given description.
            Raises ValueError if the description is not recognized.
    """

    YES = "yes"
    NO = "no"

    _valid_values = {YES, NO}

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the logical flag ("yes" or "no") for a given description.

        Args:
            description (str): The description to check (e.g., "yes" or "no").

        Returns:
            str: The logical flag ("yes" or "no").

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._valid_values:
            raise ValueError(
                f"Invalid invited-since-age-extension flag: '{description}'"
            )
        return key
