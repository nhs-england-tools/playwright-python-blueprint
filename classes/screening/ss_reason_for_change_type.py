from enum import Enum
from typing import Optional


class SSReasonForChangeType(Enum):
    """
    Enum representing reasons for change to SS (Screening Status).

    Methods:
        valid_value_id: Returns the unique identifier for the reason.
        description: Returns the string description of the reason.
        by_valid_value_id(valid_value_id: int) -> Optional[SSReasonForChangeType]: Returns the enum member matching the given valid value ID.
        by_description(description: str) -> Optional[SSReasonForChangeType]: Returns the enum member matching the given description.
        by_description_case_insensitive(description: str) -> Optional[SSReasonForChangeType]: Returns the enum member matching the given description (case-insensitive).
    """

    AGE_EXTENSION_FIRST_CALL = (20415, "Age Extension First Call")
    AGE_EXTENSION_FIRST_CALL_MAY_SELF_REFER = (
        20413,
        "Age Extension First Call - May Self-refer",
    )
    AGE_EXTENSION_UN_CEASE = (20414, "Age Extension Uncease")
    AGE_EXTENSION_UN_CEASE_MAY_SELF_REFER = (
        20412,
        "Age Extension Uncease - May Self-refer",
    )
    CANCELLED_REGISTRATION = (11313, "Cancelled Registration")
    CLINICAL_REASON = (11311, "Clinical Reason")
    DATE_OF_BIRTH_AMENDMENT = (205267, "Date of birth amendment")
    DECEASED = (11309, "Deceased")
    DISCHARGE_CANNOT_CONTACT = (
        20006,
        "Discharge from Surveillance - Cannot Contact Patient",
    )
    DISCHARGE_CLINICAL_DECISION = (
        20007,
        "Discharge from Surveillance - Clinical Decision",
    )
    DISCHARGE_NATIONAL_GUIDELINES = (
        20004,
        "Discharge from Surveillance - National Guidelines",
    )
    DISCHARGE_PATIENT_CHOICE = (20005, "Discharge from Surveillance - Patient Choice")
    DISCHARGED_PATIENT_UNFIT = (20437, "Discharged, Patient Unfit")
    ELIGIBLE_FOR_SCREENING = (20424, "Eligible for Screening")
    ELIGIBLE_FS = (200641, "Eligible to be invited for FS Screening")
    FAILSAFE_TRAWL = (20426, "Failsafe Trawl")
    IMPLEMENTATION_RESET = (11323, "Implementation Reset")
    LEFT_COUNTRY = (11310, "Individual has left the country")
    INFORMAL_DEATH = (47, "Informal Death")
    INFORMED_DISSENT = (43, "Informed Dissent")
    INFORMED_DISSENT_HISTORIC = (11308, "Informed Dissent (historic)")
    INFORMED_DISSENT_VERBAL = (44, "Informed Dissent (verbal only)")
    INFORMED_DISSENT_VERBAL_HISTORIC = (
        11534,
        "Informed Dissent (verbal only) (historic)",
    )
    LATE_RESPONSE = (200510, "Late Response")
    LOST_PATIENT_CONTACT = (20156, "Lost Patient Contact")
    MANUAL_FAILSAFE = (11324, "Manual Failsafe")
    MOVE_OUT_OF_IMPLEMENTATION = (11535, "Move out of Implementation")
    MULTIPLE_DOB_CHANGES = (202447, "Multiple Date of Birth Changes")
    NO_COLON_PROGRAMME_ASSESSED = (46, "No Colon (programme assessed)")
    NO_COLON_SUBJECT_REQUEST = (45, "No Colon (subject request)")
    NOT_ELIGIBLE_FS = (200642, "No longer eligible to be invited for FS Screening")
    OPT_IN = (305717, "Opt-in")
    OPT_BACK = (11317, "Opt (Back) into Screening Programme")
    OPT_IN_ERROR = (11530, "Opt-in due to Error")
    OUTSIDE_POPULATION = (11312, "Outside Screening Population")
    PATIENT_CHOICE = (20157, "Patient Choice")
    RECALL = (11404, "Recall")
    REINSTATE_SURVEILLANCE = (20264, "Reinstate Surveillance")
    REINSTATE_DUE_TO_ERROR = (20263, "Reinstate Surveillance due to Error")
    REINSTATE_REVERSAL_DEATH = (
        11564,
        "Reinstate Surveillance for Reversal of Death Notification",
    )
    REOPENED_EPISODE = (11327, "Reopened Episode")
    REOPENED_FS_EPISODE = (205011, "Reopened FS Episode")
    IMMEDIATE_SCREENING = (65, "Request for Immediate Screening Episode")
    RESET_PAUSED_CEASED = (20451, "Reset after being Paused and Ceased")
    RESET_TO_CALL = (11320, "Reset seeking further data to Call")
    RESET_TO_FS = (205007, "Reset seeking further data to FS Screening")
    RESET_TO_INACTIVE = (11321, "Reset seeking further data to Inactive")
    RESET_TO_LYNCH = (307079, "Reset seeking further data to Lynch Surveillance")
    RESET_TO_LYNCH_SR = (307135, "Reset seeking further data to Lynch Self-referral")
    RESET_TO_OPTIN = (11528, "Reset seeking further data to Opt-In")
    RESET_TO_RECALL = (11322, "Reset seeking further data to Recall")
    RESET_TO_SELF_REFERRAL = (11529, "Reset seeking further data to Self-referral")
    RESET_TO_SURVEILLANCE = (20299, "Reset seeking further data to Surveillance")
    RESET_TO_BOWEL_SCOPE = (203183, "Reset seeking further data to bowel scope")
    RESULT_CANCER_TREATMENT = (11326, "Result referred for Cancer Treatment")
    RESULT_TO_SURVEILLANCE = (11325, "Result referred to Surveillance")
    REVERSAL_DEATH = (11563, "Reversal of Death Notification")
    ROLLOUT_IMPLEMENTATION = (11328, "Rollout Implementation")
    SELECTED_FOR_SURVEILLANCE = (20003, "Selected for Surveillance")
    SELF_REFERRAL = (11316, "Self-Referral")
    SET_TO_CALL_RECALL = (203055, "Set Seeking Further Data to Call/Recall")
    UNCERTIFIED_DEATH = (11314, "Uncertified Death")
    UNCONFIRMED_CLINICAL_HISTORIC = (11315, "Unconfirmed Clinical Reason (historic)")
    ELIGIBLE_FOR_LYNCH = (306447, "Eligible for Lynch surveillance")
    LYNCH_SURVEILLANCE = (305689, "Lynch Surveillance")
    BOWEL_SCOPE_DECOMMISSIONED = (307051, "Bowel scope decommissioned")

    def __init__(self, valid_value_id: int, description: str):
        """
        Initialize an SSReasonForChangeType enum member.

        Args:
            valid_value_id (int): The unique identifier for the reason.
            description (str): The string description of the reason.
        """
        self._value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique identifier for the reason.

        Returns:
            int: The valid value ID.
        """
        return self._value_id

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
    ) -> Optional["SSReasonForChangeType"]:
        """
        Returns the enum member matching the given valid value ID.

        Args:
            valid_value_id (int): The valid value ID to search for.

        Returns:
            Optional[SSReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.valid_value_id == valid_value_id), None
        )

    @classmethod
    def by_description(cls, description: str) -> Optional["SSReasonForChangeType"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SSReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next((item for item in cls if item.description == description), None)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["SSReasonForChangeType"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SSReasonForChangeType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.description.lower() == description.lower()),
            None,
        )
