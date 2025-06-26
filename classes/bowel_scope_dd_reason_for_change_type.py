from enum import Enum
from typing import Optional, Dict


class BowelScopeDDReasonForChangeType(Enum):
    """
    Enum representing reasons for change to Bowel Scope Due Date.

    Attributes:
        Ceased: Ceased
        DateOfBirthAmendment: Date of birth amendment
        EligibleToBeInvitedForFsScreening: Eligible to be invited for FS Screening
        FsScreeningEpisodeOpened: FS Screening episode opened
        MultipleDateOfBirthChanges: Multiple Date of Birth Changes
        NoLongerEligibleToBeInvitedForFsScreening: No longer eligible to be invited for FS Screening
        ReopenedFsEpisode: Reopened FS Episode
        SeekingFurtherData: Seeking further data
    """

    Ceased = (200669, "Ceased")
    DateOfBirthAmendment = (205266, "Date of birth amendment")
    EligibleToBeInvitedForFsScreening = (
        200685,
        "Eligible to be invited for FS Screening",
    )
    FsScreeningEpisodeOpened = (205002, "FS Screening episode opened")
    MultipleDateOfBirthChanges = (202426, "Multiple Date of Birth Changes")
    NoLongerEligibleToBeInvitedForFsScreening = (
        200668,
        "No longer eligible to be invited for FS Screening",
    )
    ReopenedFsEpisode = (205012, "Reopened FS Episode")
    SeekingFurtherData = (200670, "Seeking further data")

    def __init__(self, valid_value_id: int, description: str):
        """
        Initialize a BowelScopeDDReasonForChangeType enum member.

        Args:
            valid_value_id (int): The unique identifier for the reason.
            description (str): The string description of the reason.
        """
        self._valid_value_id: int = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique identifier for the reason.

        Returns:
            int: The valid value ID.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the string description of the reason.

        Returns:
            str: The description.
        """
        return self._description

    @classmethod
    def _descriptions(cls) -> Dict[str, "BowelScopeDDReasonForChangeType"]:
        """
        Returns a mapping from description to enum member.

        Returns:
            Dict[str, BowelScopeDDReasonForChangeType]: Mapping from description to enum member.
        """
        return {item.description: item for item in cls}

    @classmethod
    def _lowercase_descriptions(cls) -> Dict[str, "BowelScopeDDReasonForChangeType"]:
        """
        Returns a mapping from lowercase description to enum member.

        Returns:
            Dict[str, BowelScopeDDReasonForChangeType]: Mapping from lowercase description to enum member.
        """
        return {item.description.lower(): item for item in cls}

    @classmethod
    def _valid_value_ids(cls) -> Dict[int, "BowelScopeDDReasonForChangeType"]:
        """
        Returns a mapping from valid value ID to enum member.

        Returns:
            Dict[int, BowelScopeDDReasonForChangeType]: Mapping from valid value ID to enum member.
        """
        return {item.valid_value_id: item for item in cls}

    @classmethod
    def by_description(
        cls, description: Optional[str]
    ) -> Optional["BowelScopeDDReasonForChangeType"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (Optional[str]): The description to search for.

        Returns:
            Optional[BowelScopeDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        if description is None:
            return None
        return cls._lowercase_descriptions().get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["BowelScopeDDReasonForChangeType"]:
        """
        Returns the enum member matching the given valid value ID.

        Args:
            valid_value_id (int): The valid value ID to search for.

        Returns:
            Optional[BowelScopeDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        return cls._valid_value_ids().get(valid_value_id)
