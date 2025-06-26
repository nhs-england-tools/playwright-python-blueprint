class AppointmentSlotType:
    """
    Utility class for mapping symbolic appointment slot types to their internal IDs.

    This class provides a mapping between human-readable appointment slot type descriptions
    (such as "clinic", "phone", "video") and their corresponding internal integer IDs used in the system.

    Methods:
        get_id(description: str) -> int:
            Returns the internal ID for a given appointment slot type description.
            Raises ValueError if the description is not recognized.
    """

    _mapping = {
        "clinic": 1001,
        "phone": 1002,
        "video": 1003,
        # Add more mappings here as needed
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the internal ID for a given appointment slot type description.

        Args:
            description (str): The appointment slot type description (e.g., "clinic").

        Returns:
            int: The internal ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._mapping:
            raise ValueError(f"Unknown appointment slot type: {description}")
        return cls._mapping[key]
