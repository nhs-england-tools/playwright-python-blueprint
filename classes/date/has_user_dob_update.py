from enum import Enum
from typing import Optional


class HasUserDobUpdate(Enum):
    """
    Enum representing whether a subject has a user-initiated date of birth update.

    Members:
        NO: No user DOB update.
        YES: Has a user DOB update.

    Methods:
        by_description(description: str) -> Optional[HasUserDobUpdate]:
            Returns the enum member matching the given description, or None if not found.
        get_description() -> str:
            Returns the string description of the enum member.
    """

    NO = "No"
    YES = "Yes"

    @classmethod
    def by_description(cls, description: str) -> Optional["HasUserDobUpdate"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[HasUserDobUpdate]: The matching enum member, or None if not found.
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
