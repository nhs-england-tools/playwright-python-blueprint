from enum import Enum
from typing import Optional, Dict


class HasReferralDate(Enum):
    """
    Enum representing referral date criteria with descriptions.
    """

    MORE_THAN_28_DAYS_AGO = "more than 28 days ago"
    NO = "No"
    PAST = "past"
    YES = "Yes"
    WITHIN_THE_LAST_28_DAYS = "within the last 28 days"

    def __init__(self, description: str):
        self._description: str = description

    @property
    def description(self) -> str:
        """Returns the description for the referral date criteria."""
        return self._description

    @classmethod
    def _build_map(cls) -> None:
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, HasReferralDate] = {}
            for item in cls:
                cls._descriptions[item.description] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["HasReferralDate"]:
        """
        Returns the HasReferralDate matching the given description.
        """
        cls._build_map()
        return cls._descriptions.get(description)
