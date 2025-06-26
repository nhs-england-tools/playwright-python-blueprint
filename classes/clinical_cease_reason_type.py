from enum import Enum
from typing import Optional, Dict


class ClinicalCeaseReasonType(Enum):
    """
    Enum representing clinical reasons for ceasing a subject from screening.

    Members:
        ALREADY_INVOLVED_IN_SURVEILLANCE_PROGRAMME_OUTSIDE_BCSP: Already involved in Surveillance Programme outside BCSP
        CLINICAL_ASSESSMENT_INDICATES_CEASE_SURVEILLANCE_AND_SCREENING: Clinical Assessment indicates Cease Surveillance and Screening
        CURRENTLY_UNDER_TREATMENT: Currently under treatment
        NO_FUNCTIONING_COLON: No functioning colon
        RECENT_COLONOSCOPY: Recent colonoscopy
        REFER_TO_SYMPTOMATIC_SERVICE: Refer to Symptomatic Service
        TERMINAL_ILLNESS: Terminal Illness
        UNDER_TREATMENT_FOR_ULCERATIVE_COLITIS_CROHNS_DISEASE_BOWEL_CANCER_OR_OTHER_RESULTING_IN_CEASE: Under treatment for ulcerative colitis, Crohn's disease, bowel cancer or other, resulting in cease
        UNFIT_FOR_FURTHER_INVESTIGATION: Unfit for further investigation
        NULL: Null value for subject selection criteria
        NOT_NULL: Not Null value for subject selection criteria
    """

    # BCSS values
    ALREADY_INVOLVED_IN_SURVEILLANCE_PROGRAMME_OUTSIDE_BCSP = (
        11369,
        "Already involved in Surveillance Programme outside BCSP",
    )
    CLINICAL_ASSESSMENT_INDICATES_CEASE_SURVEILLANCE_AND_SCREENING = (
        20066,
        "Clinical Assessment indicates Cease Surveillance and Screening",
    )
    CURRENTLY_UNDER_TREATMENT = (11371, "Currently under treatment")
    NO_FUNCTIONING_COLON = (11366, "No functioning colon")
    RECENT_COLONOSCOPY = (11372, "Recent colonoscopy")
    REFER_TO_SYMPTOMATIC_SERVICE = (205274, "Refer to Symptomatic Service")
    TERMINAL_ILLNESS = (11367, "Terminal Illness")
    UNDER_TREATMENT_FOR_ULCERATIVE_COLITIS_CROHNS_DISEASE_BOWEL_CANCER_OR_OTHER_RESULTING_IN_CEASE = (
        11368,
        "Under treatment for ulcerative colitis, Crohn's disease, bowel cancer or other, resulting in cease",
    )
    UNFIT_FOR_FURTHER_INVESTIGATION = (11373, "Unfit for further investigation")

    # Extra subject selection criteria values
    NULL = (None, "Null")
    NOT_NULL = (None, "Not Null")

    def __init__(self, valid_value_id: Optional[int], description: str):
        """
        Initialize a ClinicalCeaseReasonType enum member.

        Args:
            valid_value_id (Optional[int]): The unique identifier for the reason.
            description (str): The string description of the reason.
        """
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """
        Returns the unique identifier for the clinical cease reason.

        Returns:
            Optional[int]: The valid value ID.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the string description of the clinical cease reason.

        Returns:
            str: The description.
        """
        return self._description

    @classmethod
    def _build_lookup_maps(cls):
        """
        Builds lookup maps for descriptions and valid value IDs.
        """
        cls._descriptions: Dict[str, "ClinicalCeaseReasonType"] = {}
        cls._lowercase_descriptions: Dict[str, "ClinicalCeaseReasonType"] = {}
        cls._valid_value_ids: Dict[int, "ClinicalCeaseReasonType"] = {}

        for member in cls:
            if member.description:
                cls._descriptions[member.description] = member
                cls._lowercase_descriptions[member.description.lower()] = member
            if member.valid_value_id is not None:
                cls._valid_value_ids[member.valid_value_id] = member

    @classmethod
    def by_description(cls, description: str) -> Optional["ClinicalCeaseReasonType"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[ClinicalCeaseReasonType]: The matching enum member, or None if not found.
        """
        if not hasattr(cls, "_descriptions"):
            cls._build_lookup_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["ClinicalCeaseReasonType"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[ClinicalCeaseReasonType]: The matching enum member, or None if not found.
        """
        if not hasattr(cls, "_lowercase_descriptions"):
            cls._build_lookup_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["ClinicalCeaseReasonType"]:
        """
        Returns the enum member matching the given valid value ID.

        Args:
            valid_value_id (int): The valid value ID to search for.

        Returns:
            Optional[ClinicalCeaseReasonType]: The matching enum member, or None if not found.
        """
        if not hasattr(cls, "_valid_value_ids"):
            cls._build_lookup_maps()
        return cls._valid_value_ids.get(valid_value_id)
