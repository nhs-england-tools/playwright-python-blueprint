from enum import Enum
from typing import Dict, Optional


class SubjectHubCode(Enum):
    """
    Enum representing subject hub code types.

    Members:
        USER_HUB: Represents the user's hub.
        USER_ORGANISATION: Represents the user's organisation.

    Methods:
        description: Returns the string description of the enum member.
        by_description(description: str) -> Optional[SubjectHubCode]:
            Returns the enum member matching the given description, or None if not found.
    """

    USER_HUB = "user's hub"
    USER_ORGANISATION = "user's organisation"

    @property
    def description(self) -> str:
        """
        Returns the string description of the enum member.

        Returns:
            str: The description value.
        """
        return self.value

    @classmethod
    def by_description(cls, description: str) -> Optional["SubjectHubCode"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SubjectHubCode]: The matching enum member, or None if not found.
        """
        # Build reverse lookup map once and store it as a class attribute
        if not hasattr(cls, "_description_map"):
            cls._description_map: Dict[str, SubjectHubCode] = {
                member.value: member for member in cls
            }
        return cls._description_map.get(description)
