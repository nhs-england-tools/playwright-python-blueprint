from enum import Enum


class LynchIncidentEpisodeType(Enum):
    """
    Enum for mapping symbolic values used to filter Lynch incident episode linkage.

    Members:
        NULL: Represents a null value.
        NOT_NULL: Represents a not-null value.
        LATEST_EPISODE: Represents the latest episode.
        EARLIER_EPISODE: Represents an earlier episode.
    """

    NULL = "null"
    NOT_NULL = "not null"
    LATEST_EPISODE = "latest episode"
    EARLIER_EPISODE = "earlier episode"

    @classmethod
    def from_description(cls, description: str) -> "LynchIncidentEpisodeType":
        """
        Returns the Enum member for a given description.

        Args:
            description (str): The description to check.

        Returns:
            LynchIncidentEpisodeType: The corresponding Enum member.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        for member in cls:
            if member.value == key:
                return member
        raise ValueError(f"Unknown Lynch incident episode criteria: '{description}'")
