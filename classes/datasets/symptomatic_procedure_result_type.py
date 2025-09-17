from enum import Enum
from typing import Optional


class SymptomaticProcedureResultType(Enum):
    """
    Enum representing symptomatic procedure result types, mapped to valid value IDs and descriptions.
    """

    CANCER = (202016, "Cancer")
    HIGH_RISK_ADENOMA = (202015, "High risk adenoma")
    HIGH_RISK_FINDINGS = (305622, "High-risk findings")
    INTERMEDIATE_RISK_ADENOMA = (202014, "Intermediate risk adenoma")
    LNPCP = (305623, "LNPCP")
    LOW_RISK_ADENOMA = (202013, "Low risk adenoma")
    NON_NEOPLASTIC = (202012, "Non-neoplastic")
    PATIENT_UNFIT = (
        202017,
        "Patient is unfit for a symptomatic procedure at this time",
    )
    NULL = (None, "Null")

    def __init__(self, valid_value_id: Optional[int], description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """
        Returns the valid value ID for the symptomatic procedure result type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the symptomatic procedure result type.
        """
        return self._description

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["SymptomaticProcedureResultType"]:
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
    ) -> Optional["SymptomaticProcedureResultType"]:
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
        cls, valid_value_id: Optional[int]
    ) -> Optional["SymptomaticProcedureResultType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
