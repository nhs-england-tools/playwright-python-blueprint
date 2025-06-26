class SurveillanceReviewStatusType:
    """
    Utility class for mapping surveillance review status descriptions to valid value IDs.

    This class provides:
        - A mapping from human-readable surveillance review status descriptions (e.g., "awaiting review", "in progress", "completed") to their corresponding internal valid value IDs.
        - A method to retrieve the valid value ID for a given description.

    Methods:
        get_id(description: str) -> int:
            Returns the valid value ID for a given surveillance review status description.
            Raises ValueError if the description is not recognized.
    """

    _label_to_id = {
        "awaiting review": 9301,
        "in progress": 9302,
        "completed": 9303,
        # Extend if needed
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the valid value ID for a given surveillance review status description.

        Args:
            description (str): The surveillance review status description.

        Returns:
            int: The valid value ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._label_to_id:
            raise ValueError(f"Unknown surveillance review status: '{description}'")
        return cls._label_to_id[key]
