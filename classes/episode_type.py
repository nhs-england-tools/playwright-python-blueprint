from enum import Enum
from typing import Optional


class EpisodeType(Enum):
    """
    Enum representing different types of screening episodes.

    Members:
        FOBT: Faecal Occult Blood Test (short description)
        Fobt: Faecal Occult Blood Test (long description)
        BowelScope: Bowel Scope episode
        Surveillance: Surveillance episode
        LYNCH_SURVEILLANCE: Lynch Surveillance episode (long description)
        Lynch: Lynch Surveillance episode (short description)
    """

    FOBT = (11350, "FOBT")
    Fobt = (11350, "FOBT Screening")
    BowelScope = (200640, "Bowel Scope")
    Surveillance = (11351, "Surveillance")
    LYNCH_SURVEILLANCE = (305633, "Lynch Surveillance")
    Lynch = (305633, "Lynch")

    def __init__(self, valid_value_id, description):
        """
        Initialize an EpisodeType enum member.

        Args:
            valid_value_id (int): The unique identifier for the episode type.
            description (str): The string description of the episode type.
        """
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique identifier for the episode type.

        Returns:
            int: The valid value ID.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the string description of the episode type.

        Returns:
            str: The description.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["EpisodeType"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[EpisodeType]: The matching enum member, or None if not found.
        """
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["EpisodeType"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[EpisodeType]: The matching enum member, or None if not found.
        """
        for member in cls:
            if member.description.lower() == description.lower():
                return member
        return None

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["EpisodeType"]:
        """
        Returns the enum member matching the given valid value ID.

        Args:
            valid_value_id (int): The valid value ID to search for.

        Returns:
            Optional[EpisodeType]: The matching enum member, or None if not found.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
