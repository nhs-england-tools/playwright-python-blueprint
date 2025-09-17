from enum import Enum
from typing import Optional


class SurveillanceReviewCaseType(Enum):
    """
    Enum representing surveillance review case types, mapped to valid value IDs and descriptions.
    """

    AUTOMATICALLY_ADDED_CASE = (305564, "Automatically added case")
    INITIAL_MANUAL_COHORT_CASE = (305563, "Initial manual cohort case")
    QA_USER_ADDED_CASE = (305571, "QA user added case")
    SC_USER_ADDED_CASE = (305565, "SC user added case")

    def __init__(self, valid_value_id: int, description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the valid value ID for the surveillance review case type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the surveillance review case type.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["SurveillanceReviewCaseType"]:
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
    ) -> Optional["SurveillanceReviewCaseType"]:
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
    ) -> Optional["SurveillanceReviewCaseType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
