from enum import Enum
from typing import Optional


class ManualCeaseRequested(Enum):
    """
    Enum representing the manual cease request status for a subject.

    Members:
        NO: No manual cease requested.
        DISCLAIMER_LETTER_REQUIRED: Disclaimer letter required (C1).
        DISCLAIMER_LETTER_SENT: Disclaimer letter sent (C2).
        YES: Yes, manual cease requested.

    Methods:
        description: Returns the string description of the enum member.
        by_description(description: str) -> Optional[ManualCeaseRequested]:
            Returns the enum member matching the given description, or None if not found.
        by_description_case_insensitive(description: str) -> Optional[ManualCeaseRequested]:
            Returns the enum member matching the given description (case-insensitive), or None if not found.
    """

    NO = "no"
    DISCLAIMER_LETTER_REQUIRED = "yes - disclaimer letter required (c1)"
    DISCLAIMER_LETTER_SENT = "yes - disclaimer letter sent (c2)"
    YES = "yes"

    def __init__(self, description: str) -> None:
        """
        Initialize a ManualCeaseRequested enum member.

        Args:
            description (str): The string description of the manual cease request status.
        """
        self._description: str = description

    @property
    def description(self) -> str:
        """
        Returns the string description of the enum member.

        Returns:
            str: The description value.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["ManualCeaseRequested"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[ManualCeaseRequested]: The matching enum member, or None if not found.
        """
        for item in cls:
            if item.description == description:
                return item
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["ManualCeaseRequested"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[ManualCeaseRequested]: The matching enum member, or None if not found.
        """
        if description is None:
            return None
        for item in cls:
            if item.description.lower() == description.lower():
                return item
        return None
