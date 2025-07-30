from enum import Enum
from typing import Optional, Dict


class ReasonNoTreatmentReceivedType(Enum):
    """
    Enum representing reasons why no treatment was received in cancer audit datasets,
    with valid value IDs and descriptions.
    """

    ADVANCED_DISEASE = (99016, "Advanced Disease")
    DIED = (99017, "Died")
    MEDICALLY_UNFIT = (99014, "Medically Unfit")
    NO_EVIDENCE_OF_CANCER = (99061, "No Evidence of Cancer")
    PATIENT_CHOICE = (99015, "Patient Choice")
    UNKNOWN = (99018, "Unknown")

    def __init__(self, valid_value_id: int, description: str):
        self._valid_value_id: int = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the reason no treatment was received."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the reason no treatment was received."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for ReasonNoTreatmentReceivedType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, ReasonNoTreatmentReceivedType] = {}
            cls._lowercase_descriptions: Dict[str, ReasonNoTreatmentReceivedType] = {}
            cls._valid_value_ids: Dict[int, ReasonNoTreatmentReceivedType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["ReasonNoTreatmentReceivedType"]:
        """
        Returns the ReasonNoTreatmentReceivedType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["ReasonNoTreatmentReceivedType"]:
        """
        Returns the ReasonNoTreatmentReceivedType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["ReasonNoTreatmentReceivedType"]:
        """
        Returns the ReasonNoTreatmentReceivedType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """Returns the valid value ID for the reason no treatment was received."""
        return self._valid_value_id

    def get_description(self) -> str:
        """Returns the description for the reason no treatment was received."""
        return self._description
