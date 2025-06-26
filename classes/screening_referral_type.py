class ScreeningReferralType:
    """
    Utility class for mapping screening referral descriptions to valid value IDs.

    This class provides:
        - A mapping from human-readable screening referral descriptions (e.g., "gp", "self referral", "hospital") to their corresponding internal valid value IDs.
        - A method to retrieve the valid value ID for a given description.

    Methods:
        get_id(description: str) -> int:
            Returns the valid value ID for a given screening referral description.
            Raises ValueError if the description is not recognized.
    """

    _label_to_id = {
        "gp": 9701,
        "self referral": 9702,
        "hospital": 9703,
        # Add more as needed
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the valid value ID for a given screening referral description.

        Args:
            description (str): The screening referral description (e.g., "gp").

        Returns:
            int: The valid value ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._label_to_id:
            raise ValueError(f"Unknown screening referral type: '{description}'")
        return cls._label_to_id[key]
