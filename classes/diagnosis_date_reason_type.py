from enum import Enum
from typing import Optional, Dict


class DiagnosisDateReasonType(Enum):
    """
    Enum representing diagnosis date reasons with valid value IDs and descriptions.
    """

    TWO_DNAS_OF_COLONOSCOPY_ASSESSMENT_APPT = (
        305521,
        "2 DNAs of colonoscopy assessment appt",
    )
    INCORRECT_INFORMATION_PREVIOUSLY_ENTERED = (
        305501,
        "Incorrect information previously entered",
    )
    OTHER = (305500, "Other")
    PATIENT_CHOICE = (305522, "Patient choice")
    PATIENT_COULD_NOT_BE_CONTACTED = (305505, "Patient could not be contacted")
    PATIENT_DECEASED = (305503, "Patient deceased")
    PATIENT_DECLINED_ALL_APPOINTMENTS = (305520, "Patient declined all appointments")
    PATIENT_EMIGRATED = (305504, "Patient emigrated")
    REOPENED_OLD_EPISODE_DATE_UNKNOWN = (305502, "Reopened old episode, date unknown")
    SSPI_UPDATE_PATIENT_DECEASED = (305525, "SSPI update - patient deceased")
    SSPI_UPDATE_PATIENT_EMIGRATED = (305524, "SSPI update - patient emigrated")
    SYSTEM_CLOSURE_AFTER_NO_INPUT_OF_DIAGNOSIS_DATE = (
        305519,
        "System closure after no input of diagnosis date",
    )
    NULL = (None, "NULL")
    NOT_NULL = (None, "NOT NULL")

    def __init__(self, valid_value_id: Optional[int], description: str):
        self._valid_value_id: Optional[int] = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """Returns the valid value ID for the diagnosis date reason."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the diagnosis date reason."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for DiagnosisDateReasonType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, DiagnosisDateReasonType] = {}
            cls._lowercase_descriptions: Dict[str, DiagnosisDateReasonType] = {}
            cls._valid_value_ids: Dict[Optional[int], DiagnosisDateReasonType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["DiagnosisDateReasonType"]:
        """
        Returns the DiagnosisDateReasonType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["DiagnosisDateReasonType"]:
        """
        Returns the DiagnosisDateReasonType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: Optional[int]
    ) -> Optional["DiagnosisDateReasonType"]:
        """
        Returns the DiagnosisDateReasonType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_valid_value_id(self) -> Optional[int]:
        """
        Returns the valid value ID for the diagnosis date reason.
        """
        return self._valid_value_id

    def get_description(self) -> str:
        """
        Returns the description for the diagnosis date reason.
        """
        return self._description
