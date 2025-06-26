class IntendedExtentType:
    """
    Utility class for mapping intended extent values to nullability flags or valid value IDs.

    This class provides:
        - Logical flags for "null" and "not null" to indicate nullability.
        - A mapping from descriptive intended extent labels (e.g., "full", "partial", "none") to internal valid value IDs.
        - Methods to convert descriptions to flags or IDs, and to get a description from a sentinel value.

    Methods:
        from_description(description: str) -> str | int:
            Returns the logical flag ("null"/"not null") or the valid value ID for a given description.
            Raises ValueError if the description is not recognized.

        get_id(description: str) -> int:
            Returns the valid value ID for a given intended extent description.
            Raises ValueError if the description is not recognized or has no ID.

        get_description(sentinel: str) -> str:
            Returns the string description for a sentinel value ("null" or "not null").
            Raises ValueError if the sentinel is not recognized.
    """

    NULL = "null"
    NOT_NULL = "not null"

    _label_to_id = {
        "full": 9201,
        "partial": 9202,
        "none": 9203,
        # Add others as needed
    }

    _null_flags = {NULL, NOT_NULL}

    @classmethod
    def from_description(cls, description: str):
        """
        Returns the logical flag ("null"/"not null") or the valid value ID for a given description.

        Args:
            description (str): The intended extent description.

        Returns:
            str | int: The logical flag ("null"/"not null") or the valid value ID.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key in cls._null_flags:
            return key
        if key in cls._label_to_id:
            return cls._label_to_id[key]
        raise ValueError(f"Unknown intended extent: '{description}'")

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the valid value ID for a given intended extent description.

        Args:
            description (str): The intended extent description.

        Returns:
            int: The valid value ID.

        Raises:
            ValueError: If the description is not recognized or has no ID.
        """
        key = description.strip().lower()
        if key not in cls._label_to_id:
            raise ValueError(f"No ID available for intended extent: '{description}'")
        return cls._label_to_id[key]

    @classmethod
    def get_description(cls, sentinel: str) -> str:
        """
        Returns the string description for a sentinel value ("null" or "not null").

        Args:
            sentinel (str): The sentinel value to describe.

        Returns:
            str: The string description ("NULL" or "NOT NULL").

        Raises:
            ValueError: If the sentinel is not recognized.
        """
        if sentinel == cls.NULL:
            return "NULL"
        if sentinel == cls.NOT_NULL:
            return "NOT NULL"
        raise ValueError(f"Invalid sentinel: '{sentinel}'")
