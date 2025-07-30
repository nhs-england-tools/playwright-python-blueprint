from enum import Enum
from typing import Optional, Dict


class EpisodeStatusReasonType(Enum):
    """
    Enum representing episode status reasons with valid value IDs and descriptions.
    """

    BOWEL_SCOPE_DECOMMISSIONED = (307043, "Bowel scope decommissioned")
    CANCELLED_REGISTRATION = (11465, "Cancelled Registration")
    CEASE_REQUEST = (42, "Cease Request")
    CLINICAL_REASON = (11358, "Clinical Reason")
    CURRENTLY_INVOLVED_IN_A_SURVEILLANCE_PROGRAMME_OUTSIDE_BCSP = (
        200273,
        "Currently involved in a surveillance programme outside BCSP",
    )
    CURRENTLY_UNDER_CARE_FOR_CANCER = (200274, "Currently under care for cancer")
    DECEASED = (11356, "Deceased")
    DECLINE = (203050, "Decline")
    DISCHARGE_FROM_SURVEILLANCE_AGE = (20031, "Discharge from Surveillance - Age")
    DISCHARGE_FROM_SURVEILLANCE_CANNOT_CONTACT_PATIENT = (
        20034,
        "Discharge from Surveillance - Cannot Contact Patient",
    )
    DISCHARGE_FROM_SURVEILLANCE_CLINICAL_DECISION = (
        20035,
        "Discharge from Surveillance - Clinical Decision",
    )
    DISCHARGE_FROM_SURVEILLANCE_NATIONAL_GUIDELINES = (
        20032,
        "Discharge from Surveillance - National Guidelines",
    )
    DISCHARGE_FROM_SURVEILLANCE_PATIENT_CHOICE = (
        20033,
        "Discharge from Surveillance - Patient Choice",
    )
    DISCHARGE_FROM_SURVEILLANCE_PATIENT_DISSENT = (
        20038,
        "Discharge from Surveillance - Patient Dissent",
    )
    DISCHARGED = (11364, "Discharged")
    DISCHARGED_FROM_SCREENING_INTO_SYMPTOMATIC_CARE = (
        20423,
        "Discharged from Screening into Symptomatic care",
    )
    EPISODE_COMPLETE = (11360, "Episode Complete")
    INCORRECT_DATE_OF_BIRTH = (203180, "Incorrect Date of Birth")
    INDIVIDUAL_HAS_LEFT_THE_COUNTRY = (11357, "Individual has left the country")
    INFORMED_DISSENT = (11355, "Informed Dissent")
    NON_RESPONSE = (11359, "Non Response")
    NOT_SUITABLE = (203054, "Not suitable")
    OPT_OUT_OF_CURRENT_EPISODE = (200275, "Opt out of current episode")
    PATIENT_CHOICE = (20235, "Patient Choice")
    PATIENT_DISCHARGE_FROM_SURVEILLANCE = (20037, "Patient Discharge from Surveillance")
    PATIENT_COULD_NOT_BE_CONTACTED = (11467, "Patient could not be contacted")
    PATIENT_ELECTED_PRIVATE_TREATMENT = (11365, "Patient elected private treatment")
    PENDING_COMPLETION_OF_OUTSTANDING_EVENTS = (
        11363,
        "Pending Completion of Outstanding Events",
    )
    RETURNED_UNDELIVERED_MAIL = (15050, "Returned/Undelivered mail")
    RETURNED_UNDELIVERED_MAIL_LETTER_SENT = (
        203052,
        "Returned/undelivered mail letter sent",
    )
    SUBJECT_NOT_AVAILABLE_FOR_OFFERED_APPOINTMENT = (
        203051,
        "Subject not available for offered appointment",
    )
    SURVEILLANCE_POSTPONED = (20036, "Surveillance Postponed")
    SURVEILLANCE_SELECTION = (20174, "Surveillance Selection")
    UNCERTIFIED_DEATH = (11405, "Uncertified Death")
    UNCONFIRMED_CLINICAL_REASON = (11406, "Unconfirmed Clinical Reason")
    WAITING_FURTHER_ASSESSMENT = (20384, "Waiting Further Assessment")
    WAITING_FURTHER_INFORMATION = (11361, "Waiting Further Information")
    NULL = (None, "Null")

    def __init__(self, valid_value_id: Optional[int], description: str):
        self._valid_value_id: Optional[int] = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """Returns the valid value ID for the episode status reason."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the episode status reason."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for EpisodeStatusReasonType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, EpisodeStatusReasonType] = {}
            cls._lowercase_descriptions: Dict[str, EpisodeStatusReasonType] = {}
            cls._valid_value_ids: Dict[Optional[int], EpisodeStatusReasonType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["EpisodeStatusReasonType"]:
        """
        Returns the EpisodeStatusReasonType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["EpisodeStatusReasonType"]:
        """
        Returns the EpisodeStatusReasonType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: Optional[int]
    ) -> Optional["EpisodeStatusReasonType"]:
        """
        Returns the EpisodeStatusReasonType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> Optional[int]:
        """
        Returns the valid value ID for the episode status reason.
        """
        return self._valid_value_id

    def get_description(self) -> str:
        """
        Returns the description for the episode status reason.
        """
        return self._description
