class SurveillanceReviewCaseType:
    """
    Utility class for mapping surveillance review case type descriptions to valid value IDs.

    This class provides:
        - A mapping from human-readable surveillance review case type descriptions (e.g., "routine", "escalation", "clinical discussion") to their corresponding internal valid value IDs.
        - A method to retrieve the valid value ID for a given description.

    Methods:
        get_id(description: str) -> int:
            Returns the valid value ID for a given surveillance review case type description.
            Raises ValueError if the description is not recognized.
    """

    _label_to_id = {
        "routine": 9401,
        "escalation": 9402,
        "clinical discussion": 9403,
        # Extend with additional mappings as needed
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the valid value ID for a given surveillance review case type description.

        Args:
            description (str): The surveillance review case type description.

        Returns:
            int: The valid value ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._label_to_id:
            raise ValueError(f"Unknown review case type: '{description}'")
        return cls._label_to_id[key]
