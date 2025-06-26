from enum import Enum
from typing import Optional, Dict


class HasUnprocessedSSPIUpdates(Enum):
    """
    Enum representing whether a subject has unprocessed SSPI (Screening Service Provider Interface) updates.

    Members:
        NO: No unprocessed SSPI updates.
        YES: Has unprocessed SSPI updates.

    Methods:
        by_description(description: str) -> Optional[HasUnprocessedSSPIUpdates]:
            Returns the enum member matching the given description, or None if not found.
        get_description() -> str:
            Returns the string description of the enum member.
    """

    NO = "no"
    YES = "yes"

    @classmethod
    def by_description(cls, description: str) -> Optional["HasUnprocessedSSPIUpdates"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[HasUnprocessedSSPIUpdates]: The matching enum member, or None if not found.
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
