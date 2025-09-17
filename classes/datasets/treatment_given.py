from enum import Enum
from typing import Optional, Dict


class TreatmentGiven(Enum):
    """
    Enum representing types of treatment given in cancer audit datasets,
    with valid value IDs and descriptions.
    """

    CHEMOTHERAPY = (202160, "Chemotherapy")
    RADIOTHERAPY = (202163, "Radiotherapy")
    CONCURRENT_CHEMOTHERAPY_AND_RADIOTHERAPY = (
        202161,
        "Concurrent Chemotherapy And Radiotherapy",
    )
    IMMUNOTHERAPY = (202162, "Immunotherapy")
    SPECIALIST_PALLIATIVE_CARE = (202164, "Specialist Palliative Care")

    def __init__(self, valid_value_id: int, description: str):
        self._valid_value_id: int = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the treatment given."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the treatment given."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for TreatmentGiven enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, TreatmentGiven] = {}
            cls._lowercase_descriptions: Dict[str, TreatmentGiven] = {}
            cls._valid_value_ids: Dict[int, TreatmentGiven] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["TreatmentGiven"]:
        """
        Returns the TreatmentGiven matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["TreatmentGiven"]:
        """
        Returns the TreatmentGiven matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["TreatmentGiven"]:
        """
        Returns the TreatmentGiven matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """Returns the valid value ID for the treatment given."""
        return self._valid_value_id

    def get_description(self) -> str:
        """Returns the description for the treatment given."""
        return self._description
