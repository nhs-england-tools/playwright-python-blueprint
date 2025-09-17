from enum import Enum
from typing import Optional


class NotifyMessageType(Enum):
    """
    Enum representing notify message types, with description and event status ID.
    '11197' is the event status id for all S1 notify message types
    """

    NONE = ("None", None)
    S1 = ("S1", 11197)
    S1A = ("S1a", 11197)
    S1B = ("S1b", 11197)

    def __init__(self, description: str, event_status_id: Optional[int]) -> None:
        self._description = description
        self._event_status_id = event_status_id

    @property
    def description(self) -> str:
        """
        Returns the description for the notify message type.
        """
        return self._description

    @property
    def event_status_id(self) -> Optional[int]:
        """
        Returns the event status ID for the notify message type.
        """
        return self._event_status_id

    @classmethod
    def by_description(cls, description: str) -> Optional["NotifyMessageType"]:
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
    ) -> Optional["NotifyMessageType"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None
