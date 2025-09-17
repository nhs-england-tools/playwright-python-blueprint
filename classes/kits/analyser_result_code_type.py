from enum import Enum
from typing import Optional


class AnalyserResultCodeType(Enum):
    """
    Enum for analyser result code types, mapped to valid value IDs and descriptions.
    """

    ABOVE_DILUTION_RANGE = (309030, "Above dilution range")
    BELOW_MEASURING_RANGE = (309028, "Below measuring range")
    SPOILT = (309026, "Spoilt")
    TECHNICAL_FAIL = (309027, "Technical Fail")

    def __init__(self, valid_value_id: int, description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the valid value ID for the analyser result code type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the analyser result code type.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["AnalyserResultCodeType"]:
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
    ) -> Optional["AnalyserResultCodeType"]:
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
    ) -> Optional["AnalyserResultCodeType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
