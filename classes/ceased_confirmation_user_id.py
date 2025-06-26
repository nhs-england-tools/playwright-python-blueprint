from enum import Enum
from typing import Optional, Dict


class CeasedConfirmationUserId(Enum):
    """
    Enum representing possible user IDs for ceased confirmation actions.

    Members:
        AUTOMATED_PROCESS_ID: Represents an automated process user ID.
        NULL: Represents a null user ID.
        NOT_NULL: Represents a non-null user ID.
        USER_ID: Represents a specific user's ID.
    """

    AUTOMATED_PROCESS_ID = "automated process id"
    NULL = "null"
    NOT_NULL = "not null"
    USER_ID = "user's id"

    @classmethod
    def by_description(cls, description: str) -> Optional["CeasedConfirmationUserId"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[CeasedConfirmationUserId]: The matching enum member, or None if not found.
        """
        for item in cls:
            if item.value == description:
                return item
        return None

    def get_description(self) -> str:
        """
        Returns the string description of the ceased confirmation user ID.

        Returns:
            str: The description value.
        """
        return self.value
