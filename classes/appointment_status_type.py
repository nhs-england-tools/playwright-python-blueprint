class AppointmentStatusType:
    """
    Utility class for mapping descriptive appointment statuses to internal IDs.

    This class provides a mapping between human-readable appointment status descriptions
    (such as "booked", "attended", "cancelled", "dna") and their corresponding internal
    integer IDs used in the system.

    Methods:
        get_id(description: str) -> int:
            Returns the internal ID for a given appointment status description.
            Raises ValueError if the description is not recognized.
    """

    _mapping = {
        "booked": 2001,
        "attended": 2002,
        "cancelled": 2003,
        "dna": 2004,  # Did Not Attend
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the internal ID for a given appointment status description.

        Args:
            description (str): The appointment status description (e.g., "booked").

        Returns:
            int: The internal ID corresponding to the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._mapping:
            raise ValueError(f"Unknown appointment status: {description}")
        return cls._mapping[key]
