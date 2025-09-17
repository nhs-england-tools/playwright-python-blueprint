from enum import Enum
from typing import Optional


class ScreeningReferralType(Enum):
    """
    Enum representing screening referral types, mapped to valid value IDs and descriptions.
    """

    REFER_FOBT = (202010, "Refer FOBT Screening")
    REFER_LYNCH = (305702, "Refer Lynch Surveillance")
    REFER_SURVEILLANCE = (202011, "Refer Surveillance (BCSP)")
    NULL = (None, "Null")

    def __init__(self, valid_value_id: Optional[int], description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """
        Returns the valid value ID for the screening referral type.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for the screening referral type.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["ScreeningReferralType"]:
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
    ) -> Optional["ScreeningReferralType"]:
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
    ) -> Optional["ScreeningReferralType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
