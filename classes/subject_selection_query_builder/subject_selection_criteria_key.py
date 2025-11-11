from enum import Enum
from typing import Dict, Optional


class SubjectSelectionCriteriaKey(Enum):
    """
    Enum representing all possible subject selection criteria keys.

    Each member is a tuple:
        (description: str, allow_not_modifier: bool, allow_more_than_one_value: bool)

    Members:
        Each member represents a subject selection criteria key, its description, and flags indicating
        if the "not" modifier is allowed and if more than one value is allowed.

    Properties:
        description: Returns the string description of the criteria key.
        allow_not_modifier: Returns True if the "not" modifier is allowed for this key.
        allow_more_than_one_value: Returns True if more than one value is allowed for this key.

    Methods:
        by_description(description: str) -> Optional[SubjectSelectionCriteriaKey]:
            Returns the enum member matching the given description, or None if not found.
    """

    ADD_COLUMN_TO_SELECT_STATEMENT = ("add column to select statement", False, False)
    ADD_JOIN_TO_FROM_STATEMENT = ("add join to from statement", False, False)
    APPOINTMENT_DATE = ("appointment date", False, True)
    APPOINTMENT_STATUS = ("appointment status", True, True)
    APPOINTMENT_TYPE = ("appointment type", False, True)
    BOWEL_SCOPE_DUE_DATE_REASON = ("bowel scope due date reason", True, True)
    CADS_ASA_GRADE = ("cads asa grade", False, False)
    CADS_STAGING_SCANS = ("cads staging scans", False, False)
    CADS_TYPE_OF_SCAN = ("cads type of scan", False, False)
    CADS_METASTASES_PRESENT = ("cads metastases present", False, False)
    CADS_METASTASES_LOCATION = ("cads metastases location", False, False)
    CADS_METASTASES_OTHER_LOCATION = ("cads metastases other location", False, False)
    CADS_FINAL_PRE_TREATMENT_T_CATEGORY = (
        "cads final pre-treatment t category",
        False,
        False,
    )
    CADS_FINAL_PRE_TREATMENT_N_CATEGORY = (
        "cads final pre-treatment n category",
        False,
        False,
    )
    CADS_FINAL_PRETREATMENT_M_CATEGORY = (
        "cads final pre-treatment m category",
        False,
        False,
    )
    CADS_TREATMENT_RECEIVED = ("cads treatment received", False, False)
    CADS_REASON_NO_TREATMENT_RECEIVED = (
        "cads reason no treatment received",
        False,
        False,
    )
    CADS_TUMOUR_DATE_OF_DIAGNOSIS = ("cads tumour date of diagnosis", False, False)
    CADS_TUMOUR_LOCATION = ("cads tumour location", False, False)
    CADS_TUMOUR_HEIGHT_OF_TUMOUR_ABOVE_ANAL_VERGE = (
        "cads height of tumour above anal verge",
        False,
        False,
    )
    CADS_TUMOUR_PREVIOUSLY_EXCISED_TUMOUR = (
        "cads previously excised tumour (recurrence)",
        False,
        False,
    )
    CADS_TREATMENT_START_DATE = ("cads date of treatment", False, False)
    CADS_TREATMENT_TYPE = ("cads treatment type", False, False)
    CADS_TREATMENT_GIVEN = ("cads treatment given", False, False)
    CADS_CANCER_TREATMENT_INTENT = ("cads cancer treatment intent", False, False)
    CADS_TREATMENT_PROVIDER = ("cads treatment provider", False, False)
    CADS_TREATMENT_CONSULTANT = ("cads treatment consultant", False, False)
    CALCULATED_FOBT_DUE_DATE = ("calculated fobt due date", False, False)
    CALCULATED_LYNCH_DUE_DATE = ("calculated lynch due date", False, False)
    CALCULATED_SCREENING_DUE_DATE = ("calculated screening due date", False, False)
    CALCULATED_SCREENING_DUE_DATE_BIRTHDAY = (
        "calculated screening due date (birthday)",
        False,
        False,
    )
    CALCULATED_SURVEILLANCE_DUE_DATE = (
        "calculated surveillance due date",
        False,
        False,
    )
    CEASED_CONFIRMATION_DATE = ("ceased confirmation date", False, False)
    CEASED_CONFIRMATION_DETAILS = ("ceased confirmation details", True, False)
    CEASED_CONFIRMATION_USER_ID = ("ceased confirmation user id", True, False)
    CLINICAL_REASON_FOR_CEASE = ("clinical reason for cease", True, False)
    DATE_OF_DEATH = ("date of death", False, False)
    DEMOGRAPHICS_TEMPORARY_ADDRESS = ("subject has temporary address", False, False)
    DIAGNOSTIC_TEST_CONFIRMED_DATE = ("diagnostic test confirmed date", False, False)
    DIAGNOSTIC_TEST_CONFIRMED_TYPE = ("diagnostic test confirmed type", True, True)
    DIAGNOSTIC_TEST_FAILED = ("diagnostic test failed", False, True)
    DIAGNOSTIC_TEST_HAS_OUTCOME = ("diagnostic test has outcome", False, True)
    DIAGNOSTIC_TEST_HAS_RESULT = ("diagnostic test has result", False, True)
    DIAGNOSTIC_TEST_INTENDED_EXTENT = ("diagnostic test intended extent", True, False)
    DIAGNOSTIC_TEST_IS_VOID = ("diagnostic test is void", False, True)
    DIAGNOSTIC_TEST_PROPOSED_TYPE = ("diagnostic test proposed type", True, True)
    FOBT_PREVALENT_INCIDENT_STATUS = ("fobt prevalent/incident status", False, False)
    HAS_DIAGNOSTIC_TEST_CONTAINING_POLYP = (
        "has diagnostic test containing polyp",
        False,
        False,
    )
    HAS_EXISTING_SURVEILLANCE_REVIEW_CASE = (
        "has existing surveillance review case",
        False,
        False,
    )
    HAS_GP_PRACTICE = ("has gp practice", False, False)
    HAS_GP_PRACTICE_ASSOCIATED_WITH_SCREENING_CENTRE_CODE = (
        "has gp practice associated with screening centre code",
        False,
        False,
    )
    HAS_HAD_A_DATE_OF_DEATH_REMOVAL = ("has had a date of death removal", False, False)
    HAS_PREVIOUSLY_HAD_CANCER = ("has previously had cancer", False, False)
    INVITED_SINCE_AGE_EXTENSION = ("invited since age extension", False, False)
    KIT_HAS_ANALYSER_RESULT_CODE = ("kit has analyser result code", False, True)
    KIT_HAS_BEEN_READ = ("kit has been read", False, True)
    KIT_RESULT = ("kit result", True, True)
    LATEST_EPISODE_ACCUMULATED_RESULT = (
        "latest episode accumulated result",
        True,
        False,
    )
    LATEST_EPISODE_COMPLETED_SATISFACTORILY = (
        "latest episode completed satisfactorily",
        False,
        False,
    )
    LATEST_EPISODE_DATASET_INTENDED_EXTENT = (
        "latest episode dataset intended extent",
        False,
        False,
    )
    LATEST_EPISODE_DIAGNOSIS_DATE_REASON = (
        "latest episode diagnosis date reason",
        True,
        True,
    )
    LATEST_EPISODE_DOES_NOT_INCLUDE_EVENT_CODE = (
        "latest episode does not include event code",
        False,
        True,
    )
    LATEST_EPISODE_DOES_NOT_INCLUDE_EVENT_STATUS = (
        "latest episode does not include event status",
        False,
        True,
    )
    LATEST_EPISODE_ENDED = ("latest episode ended", False, False)
    LATEST_EPISODE_HAS_CANCER_AUDIT_DATASET = (
        "latest episode has cancer audit dataset",
        False,
        False,
    )
    LATEST_EPISODE_HAS_COLONOSCOPY_ASSESSMENT_DATASET = (
        "latest episode has colonoscopy assessment dataset",
        False,
        False,
    )
    LATEST_EPISODE_HAS_MDT_DATASET = ("latest episode has mdt dataset", False, False)
    LATEST_EPISODE_HAS_DIAGNOSIS_DATE = (
        "latest episode has diagnosis date",
        False,
        False,
    )
    LATEST_EPISODE_HAS_DIAGNOSTIC_TEST = (
        "latest episode has diagnostic test",
        False,
        False,
    )
    LATEST_EPISODE_HAS_REFERRAL_DATE = (
        "latest episode has referral date",
        False,
        False,
    )
    LATEST_EPISODE_HAS_SIGNIFICANT_KIT_RESULT = (
        "latest episode has significant kit result",
        False,
        False,
    )
    LATEST_EPISODE_INCLUDES_EVENT_STATUS = (
        "latest episode includes event status",
        False,
        True,
    )
    LATEST_EPISODE_INCLUDES_EVENT_CODE = (
        "latest episode includes event code",
        False,
        True,
    )
    LATEST_EPISODE_KIT_CLASS = ("latest episode kit class", True, False)
    LATEST_EPISODE_LATEST_INVESTIGATION_DATASET = (
        "latest episode latest investigation dataset",
        False,
        False,
    )
    LATEST_EPISODE_RECALL_CALCULATION_METHOD = (
        "latest episode recall calculation method",
        True,
        False,
    )
    LATEST_EPISODE_RECALL_EPISODE_TYPE = (
        "latest episode recall episode type",
        True,
        False,
    )
    LATEST_EPISODE_RECALL_SURVEILLANCE_TYPE = (
        "latest episode recall surveillance type",
        True,
        False,
    )
    LATEST_EPISODE_STARTED = ("latest episode started", False, False)
    LATEST_EPISODE_STATUS = ("latest episode status", True, False)
    LATEST_EPISODE_STATUS_REASON = ("latest episode status reason", True, True)
    LATEST_EPISODE_SUB_TYPE = ("latest episode sub-type", True, False)
    LATEST_EPISODE_TYPE = ("latest episode type", True, False)
    LATEST_EVENT_STATUS = ("latest event status", True, False)
    LYNCH_DIAGNOSIS_DATE = ("lynch diagnosis date", False, False)
    LYNCH_DUE_DATE = ("lynch due date", False, False)
    LYNCH_DUE_DATE_DATE_OF_CHANGE = ("lynch due date date of change", False, False)
    LYNCH_DUE_DATE_REASON = ("lynch due date reason", True, True)
    LYNCH_INCIDENT_EPISODE = ("lynch incident episode", False, False)
    LYNCH_LAST_COLONOSCOPY_DATE = ("lynch last colonoscopy date", False, False)
    MANUAL_CEASE_REQUESTED = ("manual cease requested", False, False)
    NOTE_COUNT = ("note count", False, False)
    NOTIFY_ARCHIVED_MESSAGE_STATUS = ("notify archived message status", False, False)
    NOTIFY_QUEUED_MESSAGE_STATUS = ("notify queued message status", False, False)
    NHS_NUMBER = ("nhs number", False, False)
    PRE_INTERRUPT_EVENT_STATUS = ("pre-interrupt event status", True, True)
    PREVIOUS_LYNCH_DUE_DATE = ("previous lynch due date", False, False)
    PREVIOUS_SCREENING_DUE_DATE = ("previous screening due date", False, False)
    PREVIOUS_SCREENING_DUE_DATE_BIRTHDAY = (
        "previous screening due date (birthday)",
        False,
        False,
    )
    PREVIOUS_SCREENING_STATUS = ("previous screening status", True, True)
    PREVIOUS_SURVEILLANCE_DUE_DATE = ("previous surveillance due date", False, False)
    REASON_FOR_ONWARD_REFERRAL = ("reason for onward referral", False, False)
    REASON_FOR_SYMPTOMATIC_REFERRAL = ("reason for symptomatic referral", False, False)
    REFER_ANOTHER_DIAGNOSTIC_TEST_TYPE = (
        "refer another diagnostic test type",
        False,
        False,
    )
    REFER_FROM_SYMPTOMATIC_TYPE = ("refer from symptomatic type", False, False)
    REFER_FROM_SYMPTOMATIC_REASON = ("refer from symptomatic reason", False, False)
    RESPONSIBLE_SCREENING_CENTRE_CODE = (
        "responsible screening centre code",
        True,
        False,
    )
    SCREENING_DUE_DATE = ("screening due date", False, False)
    SCREENING_DUE_DATE_BIRTHDAY = ("screening due date (birthday)", False, False)
    SCREENING_DUE_DATE_DATE_OF_CHANGE = (
        "screening due date date of change",
        False,
        False,
    )
    SCREENING_DUE_DATE_REASON = ("screening due date reason", True, True)
    SCREENING_REFERRAL_TYPE = ("screening referral type", False, False)
    SCREENING_STATUS = ("screening status", True, True)
    SCREENING_STATUS_DATE_OF_CHANGE = ("screening status date of change", False, False)
    SCREENING_STATUS_REASON = ("screening status reason", True, True)
    SYMPTOMATIC_PROCEDURE_DATE = ("symptomatic procedure date", False, False)
    SYMPTOMATIC_PROCEDURE_RESULT = ("symptomatic procedure result", False, False)
    SUBJECT_AGE = ("subject age", False, False)
    SUBJECT_AGE_YD = ("subject age (y/d)", False, False)
    SUBJECT_HAS_AN_OPEN_EPISODE = ("subject has an open episode", False, False)
    SUBJECT_HAS_DIAGNOSTIC_TESTS = ("subject has diagnostic tests", False, False)
    SUBJECT_HAS_EPISODES = ("subject has episodes", False, False)
    SUBJECT_HAS_EVENT_STATUS = ("subject has event status", False, False)
    SUBJECT_DOES_NOT_HAVE_EVENT_STATUS = (
        "subject does not have event status",
        False,
        False,
    )
    SUBJECT_HAS_FOBT_EPISODES = ("subject has fobt episodes", False, False)
    SUBJECT_HAS_LOGGED_FIT_KITS = ("subject has logged fit kits", False, False)
    SUBJECT_HAS_UNLOGGED_KITS = ("subject has unlogged kits", False, False)
    SUBJECT_HAS_UNPROCESSED_SSPI_UPDATES = (
        "subject has unprocessed sspi updates",
        False,
        False,
    )
    SUBJECT_HAS_USER_DOB_UPDATES = ("subject has user dob updates", False, False)
    SUBJECT_HAS_LYNCH_DIAGNOSIS = ("subject has lynch diagnosis", False, False)
    SUBJECT_HAS_KIT_NOTES = ("subject has kit notes", False, False)
    SUBJECT_HUB_CODE = ("subject hub code", True, False)
    SUBJECT_LOWER_FOBT_AGE = ("subject lower fobt age", True, False)
    SUBJECT_LOWER_LYNCH_AGE = ("subject lower lynch age", False, False)
    SUBJECT_75TH_BIRTHDAY = ("subject's 75th birthday", False, False)
    SURVEILLANCE_DUE_DATE_DATE_OF_CHANGE = (
        "surveillance due date date of change",
        False,
        False,
    )
    SURVEILLANCE_DUE_DATE_REASON = ("surveillance due date reason", True, True)
    SURVEILLANCE_DUE_DATE = ("surveillance due date", False, False)
    SURVEILLANCE_REVIEW_CASE_TYPE = ("surveillance review case type", True, False)
    SURVEILLANCE_REVIEW_STATUS = ("surveillance review status", True, True)
    WHICH_APPOINTMENT = ("which appointment", False, True)
    WHICH_DIAGNOSTIC_TEST = ("which diagnostic test", False, True)
    WHICH_TEST_KIT = ("which test kit", False, True)

    def __init__(
        self,
        description: str,
        allow_not_modifier: bool,
        allow_more_than_one_value: bool,
    ):
        """
        Initialize a SubjectSelectionCriteriaKey enum member.

        Args:
            description (str): The string description of the criteria key.
            allow_not_modifier (bool): Whether the "not" modifier is allowed.
            allow_more_than_one_value (bool): Whether more than one value is allowed.
        """
        self._description = description
        self._allow_not_modifier = allow_not_modifier
        self._allow_more_than_one_value = allow_more_than_one_value

    @property
    def description(self) -> str:
        """
        Returns the string description of the criteria key.

        Returns:
            str: The description.
        """
        return self._description

    @property
    def allow_not_modifier(self) -> bool:
        """
        Returns True if the "not" modifier is allowed for this key.

        Returns:
            bool: True if allowed, False otherwise.
        """
        return self._allow_not_modifier

    @property
    def allow_more_than_one_value(self) -> bool:
        """
        Returns True if more than one value is allowed for this key.

        Returns:
            bool: True if allowed, False otherwise.
        """
        return self._allow_more_than_one_value

    @staticmethod
    def by_description(description: str) -> Optional["SubjectSelectionCriteriaKey"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SubjectSelectionCriteriaKey]: The matching enum member, or None if not found.
        """
        return _description_map.get(description)


# Build description-to-enum map
_description_map: Dict[str, SubjectSelectionCriteriaKey] = {
    key.description: key for key in SubjectSelectionCriteriaKey
}
