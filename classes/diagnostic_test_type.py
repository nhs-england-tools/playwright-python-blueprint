class DiagnosticTestType:
    """
    Utility class for mapping descriptive diagnostic test types to valid value IDs.

    This class provides:
    - A mapping between human-readable diagnostic test type descriptions (e.g., "pcr", "antigen", "lateral flow") and their corresponding internal valid value IDs.
    - A method to retrieve the valid value ID for a given description.

    Methods:
        get_valid_value_id(description: str) -> int:
            Returns the valid value ID for a given diagnostic test type description.
            Raises ValueError if the description is not recognized.
    """

    _mapping = {
        "pcr": 3001,
        "antigen": 3002,
        "lateral flow": 3003,
        # Add more mappings as needed
    }

    @classmethod
    def get_valid_value_id(cls, description: str) -> int:
        """
        Returns the valid value ID for a given diagnostic test type description.

        Args:
            description (str): The diagnostic test type description (e.g., "pcr").

        Returns:
            int: The valid value ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._mapping:
            raise ValueError(f"Unknown diagnostic test type: '{description}'")
        return cls._mapping[key]
