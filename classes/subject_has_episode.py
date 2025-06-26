from enum import Enum
from typing import Optional


class SubjectHasEpisode(Enum):
    """
    Enum representing whether a subject has an episode.

    Members:
        YES: Subject has an episode.
        NO: Subject does not have an episode.

    Methods:
        by_description(description: str) -> Optional[SubjectHasEpisode]:
            Returns the enum member matching the given description, or None if not found.
        get_description() -> str:
            Returns the string description of the enum member.
    """

    YES = "yes"
    NO = "no"

    @classmethod
    def by_description(cls, description: str) -> Optional["SubjectHasEpisode"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SubjectHasEpisode]: The matching enum member, or None if not found.
        """
        for item in cls:
            if item.value == description:
                return item
        return None

    def get_description(self) -> str:
        """
        Returns the string description of the enum member.

        Returns:
            str: The description value.
        """
        return self.value
