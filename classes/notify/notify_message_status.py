from enum import Enum
from typing import Optional


class NotifyMessageStatus(Enum):
    """
    Enum representing the status of a notify message, with utility methods for lookup by description.
    """

    NONE = "none"
    NEW = "new"
    NOT_READ = "not read"
    READ = "read"
    REQUESTED = "requested"
    SENDING = "sending"

    @property
    def description(self) -> str:
        """
        Returns the description for the notify message status.
        """
        return self.value

    @classmethod
    def by_description(cls, description: str) -> Optional["NotifyMessageStatus"]:
        """
        Returns the enum member matching the given description (case-sensitive).
        """
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["NotifyMessageStatus"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None
