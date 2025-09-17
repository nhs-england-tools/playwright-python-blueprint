from enum import Enum
from typing import Optional


class ScreeningStatusType(Enum):
    """
    Enum representing different screening status types for a subject.

    Members:
        CALL: Call status (valid_value_id=4001)
        INACTIVE: Inactive status (valid_value_id=4002)
        OPT_IN: Opt-in status (valid_value_id=4003)
        RECALL: Recall status (valid_value_id=4004)
        SELF_REFERRAL: Self-referral status (valid_value_id=4005)
        SURVEILLANCE: Surveillance status (valid_value_id=4006)
        SEEKING_FURTHER_DATA: Seeking Further Data status (valid_value_id=4007)
        CEASED: Ceased status (valid_value_id=4008)
        BOWEL_SCOPE: Bowel Scope status (valid_value_id=4009)
        LYNCH: Lynch Surveillance status (valid_value_id=306442)
        LYNCH_SELF_REFERRAL: Lynch Self-referral status (valid_value_id=307129)
        NULL: Null value for subject selection criteria (valid_value_id=0)
        NOT_NULL: Not Null value for subject selection criteria (valid_value_id=0)

    Methods:
        valid_value_id: Returns the unique identifier for the screening status.
        description: Returns the string description of the screening status.
        by_description(description: str) -> Optional[ScreeningStatusType]: Returns the enum member matching the given description.
        by_description_case_insensitive(description: str) -> Optional[ScreeningStatusType]: Returns the enum member matching the given description (case-insensitive).
        by_valid_value_id(valid_value_id: int) -> Optional[ScreeningStatusType]: Returns the enum member matching the given valid value ID.
    """

    CALL = (4001, "Call")
    INACTIVE = (4002, "Inactive")
    OPT_IN = (4003, "Opt-in")
    RECALL = (4004, "Recall")
    SELF_REFERRAL = (4005, "Self-referral")
    SURVEILLANCE = (4006, "Surveillance")
    SEEKING_FURTHER_DATA = (4007, "Seeking Further Data")
    CEASED = (4008, "Ceased")
    BOWEL_SCOPE = (4009, "Bowel Scope")
    LYNCH = (306442, "Lynch Surveillance")
    LYNCH_SELF_REFERRAL = (307129, "Lynch Self-referral")
    NULL = (0, "Null")
    NOT_NULL = (0, "Not null")

    def __init__(self, valid_value_id: int, description: str):
        """
        Initialize a ScreeningStatusType enum member.

        Args:
            valid_value_id (int): The unique identifier for the screening status.
            description (str): The string description of the screening status.
        """
        self._value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique identifier for the screening status.

        Returns:
            int: The valid value ID.
        """
        return self._value_id

    @property
    def description(self) -> str:
        """
        Returns the string description of the screening status.

        Returns:
            str: The description.
        """
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["ScreeningStatusType"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[ScreeningStatusType]: The matching enum member, or None if not found.
        """
        for item in cls:
            if item.description == description:
                return item
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["ScreeningStatusType"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[ScreeningStatusType]: The matching enum member, or None if not found.
        """
        description = description.lower()
        for item in cls:
            if item.description.lower() == description:
                return item
        return None

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["ScreeningStatusType"]:
        """
        Returns the enum member matching the given valid value ID.

        Args:
            valid_value_id (int): The valid value ID to search for.

        Returns:
            Optional[ScreeningStatusType]: The matching enum member, or None if not found.
        """
        for item in cls:
            if item.valid_value_id == valid_value_id:
                return item
        return None
