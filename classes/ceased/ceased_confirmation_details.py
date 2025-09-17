from enum import Enum
from typing import Optional


class CeasedConfirmationDetails(Enum):
    """
    Enum representing ceased confirmation details for a subject.

    Members:
        NULL: Represents a null ceased confirmation detail.
        NOT_NULL: Represents a non-null ceased confirmation detail.
    """

    NULL = "null"
    NOT_NULL = "not null"

    @classmethod
    def by_description(cls, description: str) -> Optional["CeasedConfirmationDetails"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[CeasedConfirmationDetails]: The matching enum member, or None if not found.
        """
        for item in cls:
            if item.value == description:
                return item
        return None

    def get_description(self) -> str:
        """
        Returns the string description of the ceased confirmation detail.

        Returns:
            str: The description value.
        """
        return self.value
