from enum import Enum
from typing import Optional, Dict


class ReasonForOnwardReferralType(Enum):
    """
    Enum representing reasons for onward referral with valid value IDs and descriptions.
    """

    POLYP_NOT_FULLY_EXCISED = (20321, "Polyp not Fully Excised")
    CHECK_POLYP_SITE = (20322, "Check Polyp Site")
    MULTIPLE_POLYPS_NOT_ALL_REMOVED = (20323, "Multiple Polyps, not all Removed")
    HISTOLOGY_REQUIRED = (20324, "Histology Required")
    UNEXPLAINED_SYMPTOMS = (20325, "Unexplained Symptoms")
    INTERVENTIONS_REQUIRED = (20326, "Interventions Required")
    CURRENTLY_UNSUITABLE_FOR_ENDOSCOPIC_REFERRAL = (
        20358,
        "Currently Unsuitable for Endoscopic Referral",
    )
    FURTHER_CLINICAL_ASSESSMENT = (20359, "Further Clinical Assessment")
    INCOMPLETE_COLONIC_VISUALISATION = (20481, "Incomplete Colonic Visualisation")

    def __init__(self, valid_value_id: int, description: str):
        self._valid_value_id: int = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the reason for onward referral."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the reason for onward referral."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for ReasonForOnwardReferralType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, ReasonForOnwardReferralType] = {}
            cls._lowercase_descriptions: Dict[str, ReasonForOnwardReferralType] = {}
            cls._valid_value_ids: Dict[int, ReasonForOnwardReferralType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["ReasonForOnwardReferralType"]:
        """
        Returns the ReasonForOnwardReferralType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["ReasonForOnwardReferralType"]:
        """
        Returns the ReasonForOnwardReferralType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["ReasonForOnwardReferralType"]:
        """
        Returns the ReasonForOnwardReferralType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """
        Returns the valid value ID for the reason for onward referral.
        """
        return self._valid_value_id

    def get_description(self) -> str:
        """
        Returns the description for the reason for onward referral.
        """
        return self._description
