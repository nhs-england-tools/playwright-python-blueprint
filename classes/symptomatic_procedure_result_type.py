class SymptomaticProcedureResultType:
    """
    Utility class for mapping symptomatic surgery result descriptions to valid value IDs.

    This class provides:
        - A mapping from human-readable symptomatic surgery result descriptions (e.g., "normal", "inconclusive", "cancer detected") to their corresponding internal valid value IDs.
        - A method to retrieve the valid value ID for a given description.

    Methods:
        get_id(description: str) -> int:
            Returns the valid value ID for a given symptomatic procedure result description.
            Raises ValueError if the description is not recognized.
    """

    _label_to_id = {
        "normal": 9601,
        "inconclusive": 9602,
        "cancer detected": 9603,
        # Add more as needed
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the valid value ID for a given symptomatic procedure result description.

        Args:
            description (str): The symptomatic procedure result description.

        Returns:
            int: The valid value ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._label_to_id:
            raise ValueError(f"Unknown symptomatic procedure result: '{description}'")
        return cls._label_to_id[key]
