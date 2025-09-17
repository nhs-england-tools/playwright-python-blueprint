from enum import Enum


class HasDateOfDeathRemoval(Enum):
    """
    Enum for mapping binary filter for the presence of a date-of-death removal record.
    """

    YES = "Yes"
    NO = "No"

    @classmethod
    def from_description(cls, description: str) -> "HasDateOfDeathRemoval":
        """
        Returns the Enum member for a given description.

        Args:
            description (str): The description to check (e.g., "Yes" or "No").

        Returns:
            HasDateOfDeathRemoval: The corresponding Enum member.

        Raises:
            ValueError: If the description is not recognized.
        """
        normalized = description.strip().capitalize()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(
            f"Invalid value for date-of-death removal filter: '{description}'"
        )
