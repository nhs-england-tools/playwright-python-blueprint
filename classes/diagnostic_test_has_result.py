class DiagnosticTestHasResult:
    """
    Utility class for mapping diagnostic test result descriptions to logical flags or internal IDs.

    This class provides:
        - Logical flags for "yes" and "no" results.
        - A mapping from descriptive result labels (e.g., "positive", "negative", "indeterminate") to internal valid value IDs.
        - Methods to convert descriptions to flags or IDs.

    Methods:
        from_description(description: str) -> str | int:
            Returns the logical flag ("yes"/"no") or the valid value ID for a given description.
            Raises ValueError if the description is not recognized.

        get_id(description: str) -> int:
            Returns the valid value ID for a given result description.
            Raises ValueError if the description is not recognized or has no ID.
    """

    YES = "yes"
    NO = "no"

    _label_to_id = {
        "positive": 9001,
        "negative": 9002,
        "indeterminate": 9003,
        # Add additional mappings as needed
    }

    _valid_flags = {YES, NO}

    @classmethod
    def from_description(cls, description: str):
        """
        Returns the logical flag ("yes"/"no") or the valid value ID for a given description.

        Args:
            description (str): The diagnostic test result description.

        Returns:
            str | int: The logical flag ("yes"/"no") or the valid value ID.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key in cls._valid_flags:
            return key
        if key in cls._label_to_id:
            return cls._label_to_id[key]
        raise ValueError(f"Unknown diagnostic test result description: '{description}'")

    @classmethod
    def get_id(cls, description: str) -> int:
        """
        Returns the valid value ID for a given result description.

        Args:
            description (str): The diagnostic test result description.

        Returns:
            int: The valid value ID.

        Raises:
            ValueError: If the description is not recognized or has no ID.
        """
        key = description.strip().lower()
        if key not in cls._label_to_id:
            raise ValueError(f"No ID available for result description: '{description}'")
        return cls._label_to_id[key]
