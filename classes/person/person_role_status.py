from enum import Enum
from typing import Optional


class PersonRoleStatus(Enum):
    """
    Enum representing the status of a person's role, with utility methods for lookup by description.
    """

    CURRENT = "Current"  # Role start date is today or in the past, role end date is today or in the future
    ENDED = "Ended"  # Role end date is in the past
    FUTURE = "Future"  # Role start date is in the future
    NONE = "None"  # Person has never had this role

    @property
    def description(self) -> str:
        """
        Returns the description for the person role status.
        """
        return self.value

    @classmethod
    def by_description(cls, description: str) -> Optional["PersonRoleStatus"]:
        """
        Returns the enum member matching the given description (case-sensitive).
        Args:
            description (str): The description to match. e.g., "Current".
        Returns:
            Optional[PersonRoleStatus]: The matching enum member, or None if not found.
        """
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["PersonRoleStatus"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        Args:
            description (str): The description to match. e.g., "current", "CURRENT", "CuRrEnT".
        Returns:
            Optional[PersonRoleStatus]: The matching enum member, or None if not found.
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None
