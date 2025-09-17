from enum import Enum
from typing import Optional


class AppointmentStatusType(Enum):
    """
    Enum representing appointment status types, mapped to valid value IDs and descriptions.
    """

    ATTENDED = (6121, "Attended")
    BOOKED = (6120, "Booked")
    CANCELLED = (6122, "Cancelled")
    DID_NOT_ATTEND = (6123, "Did Not Attend")

    def __init__(self, valid_value_id: int, description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the valid value ID for the appointment status type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the appointment status type.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["AppointmentStatusType"]:
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
    ) -> Optional["AppointmentStatusType"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["AppointmentStatusType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
