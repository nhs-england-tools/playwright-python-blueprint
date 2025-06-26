class LynchDueDateReasonType:
    """
    Utility class for mapping Lynch surveillance due date reason descriptions to IDs and symbolic types.

    This class provides:
        - Logical flags for "null", "not_null", and "unchanged" to indicate symbolic types.
        - A mapping from descriptive reason labels (e.g., "holiday", "clinical request", "external delay") to internal valid value IDs.
        - A method to convert descriptions to flags or IDs.

    Methods:
        from_description(description: str) -> str | int:
            Returns the logical flag ("null", "not_null", "unchanged") or the valid value ID for a given description.
            Raises ValueError if the description is not recognized.
    """

    NULL = "null"
    NOT_NULL = "not_null"
    UNCHANGED = "unchanged"

    _label_to_id = {
        "holiday": 9801,
        "clinical request": 9802,
        "external delay": 9803,
        # Extend as needed
    }

    @classmethod
    def from_description(cls, description: str):
        """
        Returns the logical flag ("null", "not_null", "unchanged") or the valid value ID for a given description.

        Args:
            description (str): The Lynch due date reason description.

        Returns:
            str | int: The symbolic flag or the valid value ID.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key in {cls.NULL, cls.NOT_NULL, cls.UNCHANGED}:
            return key
        if key in cls._label_to_id:
            return cls._label_to_id[key]
        raise ValueError(f"Unknown Lynch due date change reason: '{description}'")
