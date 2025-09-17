from enum import Enum
from typing import Optional, Dict


class RecallCalculationMethodType(Enum):
    """
    Enum representing recall calculation methods with valid value IDs and descriptions.
    """

    BELOW_FOBT_AGE_RANGE_AT_RECALL = (202009, "Below FOBT age range at recall")
    DATE_OF_LAST_PATIENT_LETTER = (20427, "Date of last patient letter")
    DIAGNOSTIC_TEST_DATE = (20386, "Diagnostic test date")
    EPISODE_END_DATE = (20387, "Episode end date")
    G92_INTERRUPT_CLOSE_DATE = (305704, "G92 Interrupt Close Date")
    INVITATION_KIT_DATE = (40004, "Invitation Kit Date")
    LAST_PRE_BCSP_COLONOSCOPY_DATE = (305726, "Last pre BCSP colonoscopy date")
    S92_INTERRUPT_CLOSE_DATE = (40005, "S92 Interrupt Close Date")
    SURVEILLANCE_REVIEW_2019_GUIDELINES = (
        305569,
        "Surveillance review 2019 guidelines",
    )
    SYMPTOMATIC_PROCEDURE_DATE = (20385, "Symptomatic Procedure Date")
    X92_INTERRUPT_USER_DATE = (40006, "X92 Interrupt User Date")
    NULL = (None, "Null")

    def __init__(self, valid_value_id: Optional[int], description: str):
        self._valid_value_id: Optional[int] = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """Returns the valid value ID for the recall calculation method."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the recall calculation method."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for RecallCalculationMethodType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, RecallCalculationMethodType] = {}
            cls._lowercase_descriptions: Dict[str, RecallCalculationMethodType] = {}
            cls._valid_value_ids: Dict[Optional[int], RecallCalculationMethodType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["RecallCalculationMethodType"]:
        """
        Returns the RecallCalculationMethodType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["RecallCalculationMethodType"]:
        """
        Returns the RecallCalculationMethodType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: Optional[int]
    ) -> Optional["RecallCalculationMethodType"]:
        """
        Returns the RecallCalculationMethodType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> Optional[int]:
        """
        Returns the valid value ID for the recall calculation method.
        """
        return self._valid_value_id

    def get_description(self) -> str:
        """
        Returns the description for the recall calculation method.
        """
        return self._description
