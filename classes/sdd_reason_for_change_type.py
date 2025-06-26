from enum import Enum
from typing import Optional


class SDDReasonForChangeType(Enum):
    """
    Enum representing reasons for change to SDD (Surveillance Due Date).

    Members:
        AGE_EXTENSION_FIRST_CALL: Age Extension First Call
        AGE_EXTENSION_RETURN_TO_RECALL: Age Extension Return to Recall
        AWAITING_FAILSAFE: Awaiting Failsafe
        CEASED: Ceased
        DATE_OF_BIRTH_AMENDMENT: Date of Birth amendment
        DISCHARGE_FROM_SCREENING_AGE: Discharge From Screening - Age
        DISCHARGE_FROM_SURVEILLANCE_AGE: Discharge from Surveillance - Age
        DISCHARGE_FROM_SURVEILLANCE_CANNOT_CONTACT_PATIENT: Discharge from Surveillance - Cannot Contact Patient
        DISCHARGE_FROM_SURVEILLANCE_CLINICAL_DECISION: Discharge from Surveillance - Clinical Decision
        DISCHARGE_FROM_SURVEILLANCE_NATIONAL_GUIDELINES: Discharge from Surveillance - National Guidelines
        DISCHARGE_FROM_SURVEILLANCE_PATIENT_CHOICE: Discharge from Surveillance - Patient Choice
        DISCHARGE_SURVEILLANCE_REVIEW_2019_GUIDELINES: Discharge, Surveillance Review, 2019 Guidelines
        DISCHARGED_PATIENT_UNFIT: Discharged, Patient Unfit
        ELIGIBLE_FOR_SCREENING: Eligible for Screening
        ELIGIBLE_TO_BE_INVITED_FOR_FS_SCREENING: Eligible to be invited for FS Screening
        FAILSAFE_TRAWL: Failsafe Trawl
        IMPLEMENTATION_RESET: Implementation Reset
        LATE_RESPONSE: Late Response
        MANUAL_CALL_RECALL_AMENDMENT: Manual Call/Recall Amendment
        MANUALLY_REFERRED_TO_SURVEILLANCE_2019_GUIDELINES: Manually Referred to Surveillance, 2019 Guidelines
        MOVE_OUT_OF_IMPLEMENTATION: Move out of Implementation
        MOVED_TO_LYNCH_SURVEILLANCE: Moved to Lynch surveillance
        MULTIPLE_DATE_OF_BIRTH_CHANGES: Multiple Date of Birth Changes
        NO_LONGER_ELIGIBLE_TO_BE_INVITED_FOR_FS_SCREENING: No longer eligible to be invited for FS Screening
        OPT_BACK_INTO_SCREENING_PROGRAMME: Opt (Back) into Screening Programme
        OPTIN_DUE_TO_ERROR: Opt-in due to Error
        POSTPONE_SURVEILLANCE_REVIEW_2019_GUIDELINES: Postpone, Surveillance Review, 2019 Guidelines
        RECALL: Recall
        REOPENED_EPISODE: Reopened Episode
        REQUEST_SCREENING_EPISODE_OUTSIDE_NORMAL_RECALL: Request screening episode outside normal recall
        RESET_AFTER_BEING_PAUSED: Reset after being Paused
        RESET_AFTER_BEING_PAUSED_AND_CEASED: Reset after being Paused and Ceased
        RESULT_REFERRED_FOR_CANCER_TREATMENT: Result Referred for Cancer treatment
        RESULT_REFERRED_TO_SURVEILLANCE: Result referred to Surveillance
        REVERSAL_OF_DEATH_NOTIFICATION: Reversal of Death Notification
        ROLLOUT_IMPLEMENTATION: Rollout Implementation
        SELFREFERRAL: Self-Referral
        NULL: Null value for subject selection criteria
        NOT_NULL: Not Null value for subject selection criteria
        UNCHANGED: Unchanged value for subject selection criteria

    Methods:
        valid_value_id: Returns the unique identifier for the reason.
        description: Returns the string description of the reason.
        by_valid_value_id(valid_value_id: int) -> Optional[SDDReasonForChangeType]: Returns the enum member matching the given valid value ID.
        by_description(description: str) -> Optional[SDDReasonForChangeType]: Returns the enum member matching the given description.
        by_description_case_insensitive(description: str) -> Optional[SDDReasonForChangeType]: Returns the enum member matching the given description (case-insensitive).
    """

    AGE_EXTENSION_FIRST_CALL = (20417, "Age Extension First Call")
    AGE_EXTENSION_RETURN_TO_RECALL = (20416, "Age Extension Return to Recall")
    AWAITING_FAILSAFE = (307057, "Awaiting Failsafe")
    CEASED = (11329, "Ceased")
    DATE_OF_BIRTH_AMENDMENT = (11567, "Date of Birth amendment")
    DISCHARGE_FROM_SCREENING_AGE = (20233, "Discharge From Screening - Age")
    DISCHARGE_FROM_SURVEILLANCE_AGE = (20044, "Discharge from Surveillance - Age")
    DISCHARGE_FROM_SURVEILLANCE_CANNOT_CONTACT_PATIENT = (
        20047,
        "Discharge from Surveillance - Cannot Contact Patient",
    )
    DISCHARGE_FROM_SURVEILLANCE_CLINICAL_DECISION = (
        20048,
        "Discharge from Surveillance - Clinical Decision",
    )
    DISCHARGE_FROM_SURVEILLANCE_NATIONAL_GUIDELINES = (
        20045,
        "Discharge from Surveillance - National Guidelines",
    )
    DISCHARGE_FROM_SURVEILLANCE_PATIENT_CHOICE = (
        20046,
        "Discharge from Surveillance - Patient Choice",
    )
    DISCHARGE_SURVEILLANCE_REVIEW_2019_GUIDELINES = (
        305547,
        "Discharge, Surveillance Review, 2019 Guidelines",
    )
    DISCHARGED_PATIENT_UNFIT = (20438, "Discharged, Patient Unfit")
    ELIGIBLE_FOR_SCREENING = (20425, "Eligible for Screening")
    ELIGIBLE_TO_BE_INVITED_FOR_FS_SCREENING = (
        203184,
        "Eligible to be invited for FS Screening",
    )
    FAILSAFE_TRAWL = (11525, "Failsafe Trawl")
    IMPLEMENTATION_RESET = (11331, "Implementation Reset")
    LATE_RESPONSE = (200511, "Late Response")
    MANUAL_CALL_RECALL_AMENDMENT = (11330, "Manual Call/Recall Amendment")
    MANUALLY_REFERRED_TO_SURVEILLANCE_2019_GUIDELINES = (
        305566,
        "Manually Referred to Surveillance, 2019 Guidelines",
    )
    MOVE_OUT_OF_IMPLEMENTATION = (11536, "Move out of Implementation")
    MOVED_TO_LYNCH_SURVEILLANCE = (306450, "Moved to Lynch surveillance")
    MULTIPLE_DATE_OF_BIRTH_CHANGES = (202446, "Multiple Date of Birth Changes")
    NO_LONGER_ELIGIBLE_TO_BE_INVITED_FOR_FS_SCREENING = (
        200671,
        "No longer eligible to be invited for FS Screening",
    )
    OPT_BACK_INTO_SCREENING_PROGRAMME = (11333, "Opt (Back) into Screening Programme")
    OPTIN_DUE_TO_ERROR = (11531, "Opt-in due to Error")
    POSTPONE_SURVEILLANCE_REVIEW_2019_GUIDELINES = (
        305548,
        "Postpone, Surveillance Review, 2019 Guidelines",
    )
    RECALL = (11334, "Recall")
    REOPENED_EPISODE = (20297, "Reopened Episode")
    REQUEST_SCREENING_EPISODE_OUTSIDE_NORMAL_RECALL = (
        200513,
        "Request screening episode outside normal recall",
    )
    RESET_AFTER_BEING_PAUSED = (20452, "Reset after being Paused")
    RESET_AFTER_BEING_PAUSED_AND_CEASED = (20453, "Reset after being Paused and Ceased")
    RESULT_REFERRED_FOR_CANCER_TREATMENT = (
        11336,
        "Result Referred for Cancer treatment",
    )
    RESULT_REFERRED_TO_SURVEILLANCE = (11335, "Result referred to Surveillance")
    REVERSAL_OF_DEATH_NOTIFICATION = (11565, "Reversal of Death Notification")
    ROLLOUT_IMPLEMENTATION = (11337, "Rollout Implementation")
    SELFREFERRAL = (11332, "Self-Referral")

    # Special values (no valid_value_id)
    NULL = (None, "null")
    NOT_NULL = (None, "not null")
    UNCHANGED = (None, "unchanged")

    def __init__(self, valid_value_id: Optional[int], description: str):
        """
        Initialize an SDDReasonForChangeType enum member.

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
    ) -> Optional["SDDReasonForChangeType"]:
        """
        Returns the enum member matching the given valid value ID.

        Args:
            valid_value_id (int): The valid value ID to search for.

        Returns:
            Optional[SDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.valid_value_id == valid_value_id), None
        )

    @classmethod
    def by_description(cls, description: str) -> Optional["SDDReasonForChangeType"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next((item for item in cls if item.description == description), None)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["SDDReasonForChangeType"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SDDReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.description.lower() == description.lower()),
            None,
        )
