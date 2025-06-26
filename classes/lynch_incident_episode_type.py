class LynchIncidentEpisodeType:
    """
    Utility class for mapping symbolic values used to filter Lynch incident episode linkage.

    This class provides:
        - Symbolic constants for filtering Lynch incident episodes, such as "null", "not_null", "latest_episode", and "earlier_episode".
        - A method to convert a description to a valid symbolic constant.

    Members:
        NULL: Represents a null value.
        NOT_NULL: Represents a not-null value.
        LATEST_EPISODE: Represents the latest episode.
        EARLIER_EPISODE: Represents an earlier episode.

    Methods:
        from_description(description: str) -> str:
            Returns the symbolic constant for a given description.
            Raises ValueError if the description is not recognized.
    """

    NULL = "null"
    NOT_NULL = "not_null"
    LATEST_EPISODE = "latest_episode"
    EARLIER_EPISODE = "earlier_episode"

    _symbolics = {NULL, NOT_NULL, LATEST_EPISODE, EARLIER_EPISODE}

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the symbolic constant for a given description.

        Args:
            description (str): The description to check.

        Returns:
            str: The symbolic constant matching the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._symbolics:
            raise ValueError(
                f"Unknown Lynch incident episode criteria: '{description}'"
            )
        return key
