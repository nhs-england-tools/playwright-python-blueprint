from enum import Enum
from typing import Optional


class AppointmentSlotType(Enum):
    """
    Enum representing appointment slot types, mapped to valid value IDs and descriptions.
    Provides utility methods for lookup by description (case-sensitive and insensitive) and by valid value ID.
    """

    COLONOSCOPY_ASSESSMENT = (209028, "Colonoscopy Assessment")
    BOWEL_SCOPE_AUTOMATIC = (200526, "FS Automatic")
    BOWEL_SCOPE_MANUAL = (200527, "FS Manual")
    POSITIVE_ASSESSMENT = (6016, "Positive Assessment")
    POST_INVESTIGATION = (6017, "Post-Investigation")
    SURVEILLANCE = (20061, "Surveillance")

    def __init__(self, valid_value_id: int, description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the valid value ID for the appointment slot type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the appointment slot type.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["AppointmentSlotType"]:
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
    ) -> Optional["AppointmentSlotType"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["AppointmentSlotType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
