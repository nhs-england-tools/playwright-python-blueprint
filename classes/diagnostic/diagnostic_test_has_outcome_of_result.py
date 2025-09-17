from enum import Enum
from typing import Optional


class DiagnosticTestHasOutcomeOfResult(Enum):
    """
    Enum representing possible outcomes of a diagnostic test, mapped to IDs and descriptions.
    'Yes' and 'No' have negative IDs to clearly mark them as special, non-database values.
    """

    NO = (-1, "No")
    YES = (-2, "Yes")
    INVESTIGATION_COMPLETE = (20360, "Investigation Complete")
    CONSENT_REFUSED_REFER_ANOTHER = (20361, "Consent Refused, Refer Another")
    WITHDRAWN_CONSENT_REFER_ANOTHER = (20362, "Withdrawn Consent, Refer Another")
    FAILED_TEST_REFER_ANOTHER = (20363, "Failed Test - Refer Another")
    REFER_ANOTHER_DIAGNOSTIC_TEST = (20364, "Refer Another Diagnostic Test")
    REFER_SURVEILLANCE_BCSP = (20365, "Refer Surveillance (BCSP)")
    REFER_SYMPTOMATIC = (20366, "Refer Symptomatic")
    REFER_MDT = (20367, "Refer MDT")
    DID_NOT_ATTEND = (20368, "Did Not Attend")
    CANCELLED = (20369, "Cancelled")
    REFER_COLONOSCOPY = (203018, "Refer Colonoscopy")
    BOOK_ANOTHER_BOWEL_SCOPE = (203019, "Book another bowel scope")
    RETURN_TO_FOBT_SCREENING = (203020, "Return to FOBT Screening")

    def __init__(self, id: int, description: str) -> None:
        self._id = id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique ID for the diagnostic test outcome.
        """
        return self._id

    @property
    def description(self) -> str:
        """
        Returns the description for the diagnostic test outcome.
        """
        return self._description

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["DiagnosticTestHasOutcomeOfResult"]:
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
    ) -> Optional["DiagnosticTestHasOutcomeOfResult"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_id(cls, id: int) -> Optional["DiagnosticTestHasOutcomeOfResult"]:
        """
        Returns the enum member matching the given ID.
        """
        for member in cls:
            if member.valid_value_id == id:
                return member
        return None
