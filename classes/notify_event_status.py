class NotifyEventStatus:
    """
    Utility class for mapping Notify event status descriptions to internal IDs.

    This class provides:
        - A mapping from Notify event status codes (e.g., "S1", "S2", "M1") to their corresponding internal IDs.
        - A method to retrieve the internal ID for a given Notify event status description.

    Methods:
        get_id(description: str) -> int:
            Returns the internal ID for a given Notify event status description.
            Raises ValueError if the description is not recognized.
    """

    _label_to_id = {
        "S1": 9901,
        "S2": 9902,
        "M1": 9903,
        # Extend as needed
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the internal ID for a given Notify event status description.

        Args:
            description (str): The Notify event status code (e.g., "S1").

        Returns:
            int: The internal ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().upper()
        if key not in cls._label_to_id:
            raise ValueError(f"Unknown Notify event type: '{description}'")
        return cls._label_to_id[key]
