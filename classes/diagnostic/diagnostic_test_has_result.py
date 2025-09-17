from enum import Enum
from typing import Optional


class DiagnosticTestHasResult(Enum):
    """
    Enum representing possible results of a diagnostic test, mapped to IDs and descriptions.
    """

    NO = (-1, "No")
    YES = (-2, "Yes")
    NO_RESULT = (20311, "No Result")
    NORMAL = (20312, "Normal (No Abnormalities Found)")
    ABNORMAL = (20313, "Abnormal")
    LOW_RISK_ADENOMA = (20314, "Low-risk Adenoma")
    INTERMEDIATE_RISK_ADENOMA = (20315, "Intermediate-risk Adenoma")
    HIGH_RISK_ADENOMA = (20316, "High-risk Adenoma")
    CANCER_DETECTED = (20317, "Cancer Detected")
    ABNORMAL_PROCEDURE_INCOMPLETE = (20318, "Abnormal, procedure incomplete")
    HIGH_RISK_FINDINGS = (305606, "High-risk findings")
    LNPCP = (305607, "LNPCP")

    def __init__(self, id: int, description: str) -> None:
        self._id = id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique ID for the diagnostic test result.
        """
        return self._id

    @property
    def description(self) -> str:
        """
        Returns the description for the diagnostic test result.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["DiagnosticTestHasResult"]:
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
    ) -> Optional["DiagnosticTestHasResult"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_id(cls, id: int) -> Optional["DiagnosticTestHasResult"]:
        """
        Returns the enum member matching the given ID.
        """
        for member in cls:
            if member.valid_value_id == id:
                return member
        return None
