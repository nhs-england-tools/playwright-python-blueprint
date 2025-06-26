from enum import Enum
from typing import Optional


class LynchSDDReasonForChangeType(Enum):
    """
    Enum representing reasons for change to Lynch SDD (Surveillance Due Date).

    Methods:
        valid_value_id: Returns the unique identifier for the reason.
        description: Returns the string description of the reason.
        by_valid_value_id(valid_value_id: int) -> Optional[LynchSDDReasonForChangeType]: Returns the enum member matching the given valid value ID.
        by_description(description: str) -> Optional[LynchSDDReasonForChangeType]: Returns the enum member matching the given description.
        by_description_case_insensitive(description: str) -> Optional[LynchSDDReasonForChangeType]: Returns the enum member matching the given description (case-insensitive).
    """

    CEASED = (305690, "Ceased")
    DATE_OF_BIRTH_AMENDMENT = (306456, "Date of Birth amendment")
    DISCHARGED_PATIENT_UNFIT = (305693, "Discharged, Patient Unfit")
    LYNCH_SURVEILLANCE = (305684, "Lynch Surveillance")
    SELF_REFERRAL = (307130, "Self-referral")
    OPT_IN = (305718, "Opt-in")
    OPT_BACK_INTO_SCREENING_PROGRAMME = (305711, "Opt (Back) into Screening Programme")
    OPT_IN_DUE_TO_ERROR = (305712, "Opt-in due to Error")
    REOPENED_EPISODE = (305706, "Reopened Episode")
    RESULT_REFERRED_FOR_CANCER_TREATMENT = (
        305692,
        "Result referred for Cancer Treatment",
    )
    REVERSAL_OF_DEATH_NOTIFICATION = (305713, "Reversal of Death Notification")
    SELECTED_FOR_LYNCH_SURVEILLANCE = (307071, "Selected for Lynch Surveillance")
    NULL = (None, "null")
    NOT_NULL = (None, "not null")
    UNCHANGED = (None, "unchanged")

    def __init__(self, valid_value_id: Optional[int], description: str):
        """
        Initialize a LynchSDDReasonForChangeType enum member.

        Args:
            valid_value_id (Optional[int]): The unique identifier for the reason.
            description (str): The string description of the reason.
        """
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """
        Returns the unique identifier for the reason.

        Returns:
            Optional[int]: The valid value ID.
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
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["LynchSDDReasonForChangeType"]:
        """
        Returns the enum member matching the given valid value ID.

        Args:
            valid_value_id (int): The valid value ID to search for.

        Returns:
            Optional[LynchSDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.valid_value_id == valid_value_id), None
        )

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["LynchSDDReasonForChangeType"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[LynchSDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next((item for item in cls if item.description == description), None)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["LynchSDDReasonForChangeType"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[LynchSDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.description.lower() == description.lower()),
            None,
        )
