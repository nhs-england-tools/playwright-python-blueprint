class EpisodeResultType:
    """
    Utility class for mapping episode result type descriptions to logical flags or valid value IDs.

    This class provides:
        - Logical flags for "null", "not_null", and "any_surveillance_non_participation".
        - A mapping from descriptive result labels (e.g., "normal", "abnormal", "surveillance offered") to internal valid value IDs.
        - A method to convert descriptions to flags or IDs.

    Methods:
        from_description(description: str) -> str | int:
            Returns the logical flag or the valid value ID for a given description.
            Raises ValueError if the description is not recognized.
    """

    NULL = "null"
    NOT_NULL = "not_null"
    ANY_SURVEILLANCE_NON_PARTICIPATION = "any_surveillance_non_participation"

    _label_to_id = {
        "normal": 9501,
        "abnormal": 9502,
        "surveillance offered": 9503,
        # Add real mappings as needed
    }

    @classmethod
    def from_description(cls, description: str):
        """
        Returns the logical flag or the valid value ID for a given description.

        Args:
            description (str): The episode result type description.

        Returns:
            str | int: The logical flag or the valid value ID.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key in {cls.NULL, cls.NOT_NULL, cls.ANY_SURVEILLANCE_NON_PARTICIPATION}:
            return key
        if key in cls._label_to_id:
            return cls._label_to_id[key]
        raise ValueError(f"Unknown episode result type: '{description}'")
