from enum import Enum
from typing import Optional


class EpisodeResultType(Enum):
    NO_RESULT = (20311, "No Result")
    NORMAL = (20312, "Normal (No Abnormalities Found)")
    LOW_RISK_ADENOMA = (20314, "Low-risk Adenoma")
    INTERMEDIATE_RISK_ADENOMA = (20315, "Intermediate-risk Adenoma")
    HIGH_RISK_ADENOMA = (20316, "High-risk Adenoma")
    CANCER_DETECTED = (20317, "Cancer Detected")
    ABNORMAL = (20313, "Abnormal")
    CANCER_NOT_CONFIRMED = (305001, "Cancer not confirmed")
    HIGH_RISK_FINDINGS = (305606, "High-risk findings")
    LNPCP = (305607, "LNPCP")
    BOWEL_SCOPE_NON_PARTICIPATION = (605002, "Bowel scope non-participation")
    FOBT_INADEQUATE_PARTICIPATION = (605003, "FOBt inadequate participation")
    DEFINITIVE_NORMAL_FOBT_OUTCOME = (605005, "Definitive normal FOBt outcome")
    DEFINITIVE_ABNORMAL_FOBT_OUTCOME = (605006, "Definitive abnormal FOBt outcome")
    HIGH_RISK_FINDINGS_SURVEILLANCE_NON_PARTICIPATION = (
        305619,
        "High-risk findings Surveillance non-participation",
    )
    LNPCP_SURVEILLANCE_NON_PARTICIPATION = (
        305618,
        "LNPCP Surveillance non-participation",
    )
    HIGH_RISK_SURVEILLANCE_NON_PARTICIPATION = (
        605004,
        "High-risk Surveillance non-participation",
    )
    INTERMEDIATE_RISK_SURVEILLANCE_NON_PARTICIPATION = (
        605007,
        "Intermediate-risk Surveillance non-participation",
    )
    LYNCH_NON_PARTICIPATION = (305688, "Lynch non-participation")
    ANY_SURVEILLANCE_NON_PARTICIPATION = (0, "(Any) Surveillance non-participation")
    NULL = (0, "Null")
    NOT_NULL = (0, "Not Null")

    def __init__(self, valid_value_id: int, description: str):
        self._id = valid_value_id
        self._description = description

    @property
    def id(self) -> int:
        """Return the valid value ID."""
        return self._id

    @property
    def description(self) -> str:
        """Return the description."""
        return self._description

    @classmethod
    def by_id(cls, valid_value_id: int) -> Optional["EpisodeResultType"]:
        """Find an EpisodeResultType by its ID (returns first match if duplicates)."""
        return next((m for m in cls if m.id == valid_value_id), None)

    @classmethod
    def by_description(cls, description: str) -> Optional["EpisodeResultType"]:
        """Find an EpisodeResultType by its description (case-sensitive)."""
        return next((m for m in cls if m.description == description), None)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["EpisodeResultType"]:
        """Find an EpisodeResultType by its description (case-insensitive)."""
        description = description.lower()
        return next((m for m in cls if m.description.lower() == description), None)

    def __str__(self) -> str:
        """Return a string representation of the EpisodeResultType."""
        return f"{self.name} ({self.id}: {self.description})"
