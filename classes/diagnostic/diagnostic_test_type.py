from enum import Enum
from typing import Optional


class DiagnosticTestType(Enum):
    """
    Enum representing diagnostic test types, mapped to valid value IDs, descriptions, categories, and allowed status.
    Provides utility methods for lookup by description (case-sensitive and insensitive) and by valid value ID.
    'ANY' is a special placeholder representing a wildcard or default fallback when a specific diagnostic test type is not required.
    """

    BARIUM_ENEMA = (16003, "Barium Enema", "RADIOLOGY", "DISALLOWED")
    CT_COLONOGRAPHY = (16087, "CT Colonography", "RADIOLOGY", "ALLOWED")
    COLONOSCOPY = (16002, "Colonoscopy", "COLONOSCOPY", "ALLOWED")
    FLEXIBLE_SIGMOIDOSCOPY = (16004, "Flexible Sigmoidoscopy", "COLONOSCOPY", "ALLOWED")
    LIMITED_COLONOSCOPY = (17996, "Limited Colonoscopy", "COLONOSCOPY", "ALLOWED")
    NHS_BOWEL_SCOPE = (200554, "NHS bowel scope", "COLONOSCOPY", "ALLOWED")
    SCAN_XRAY = (16005, "Scan (x-ray)", "RADIOLOGY", "DISALLOWED")
    STANDARD_ABDOMINO_PELVIC_CT_SCAN = (
        16088,
        "Standard Abdomino-pelvic CT Scan",
        "RADIOLOGY",
        "DISALLOWED",
    )
    ANY = (0, "Any", "", "")

    def __init__(
        self, valid_value_id: int, description: str, category: str, allowed: str
    ) -> None:
        self._valid_value_id = valid_value_id
        self._description = description
        self._category = category
        self._allowed = allowed

    @property
    def valid_value_id(self) -> int:
        """
        Returns the valid value ID for the diagnostic test type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the diagnostic test type.
        """
        return self._description

    @property
    def category(self) -> str:
        """
        Returns the category for the diagnostic test type.
        """
        return self._category

    @property
    def allowed(self) -> str:
        """
        Returns the allowed status for the diagnostic test type.
        """
        return self._allowed

    @classmethod
    def by_description(cls, description: str) -> Optional["DiagnosticTestType"]:
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
    ) -> Optional["DiagnosticTestType"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["DiagnosticTestType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
