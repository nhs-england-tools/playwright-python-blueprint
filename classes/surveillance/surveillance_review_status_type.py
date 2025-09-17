from enum import Enum
from typing import Optional


class SurveillanceReviewStatusType(Enum):
    """
    Enum representing surveillance review status types, mapped to valid value IDs and descriptions.
    """

    AUTO_CLOSED_OUT_OF_DATE = (305560, "Auto Closed - Out of Date")
    IN_REVIEW_AT_SC = (305538, "In Review at SC")
    NEEDS_REVIEW_BY_QA = (305541, "Needs Review by QA")
    QA_CONFIRM_COMPLETE = (305543, "QA Confirm Complete")
    QA_REFER_TO_SC = (305542, "QA Refer to SC")
    REVIEW_REQUIRED = (305536, "Review Required")
    SC_CONFIRM_COMPLETE = (305539, "SC Confirm Complete")

    def __init__(self, valid_value_id: int, description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the valid value ID for the surveillance review status type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the surveillance review status type.
        """
        return self._description

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["SurveillanceReviewStatusType"]:
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
    ) -> Optional["SurveillanceReviewStatusType"]:
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
    ) -> Optional["SurveillanceReviewStatusType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
