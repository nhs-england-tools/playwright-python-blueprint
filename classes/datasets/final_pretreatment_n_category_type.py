from enum import Enum
from typing import Optional, Dict


class FinalPretreatmentNCategoryType(Enum):
    """
    Enum representing final pretreatment N categories for cancer audit datasets,
    with valid value IDs and descriptions.
    """

    CNX = (202201, "Regional lymph nodes cannot be assessed (cNX)")
    CN0 = (17256, "No regional lymph node metastasis (cN0)")
    CN1 = (17257, "Metastasis in 1 to 3 regional lymph nodes (cN1)")
    CN2 = (17258, "Metastasis in 4 or more regional lymph nodes (cN2)")
    NOT_REPORTED = (202140, "Not Reported")

    def __init__(self, valid_value_id: int, description: str):
        self._valid_value_id: int = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the N category."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the N category."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for FinalPretreatmentNCategoryType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, FinalPretreatmentNCategoryType] = {}
            cls._lowercase_descriptions: Dict[str, FinalPretreatmentNCategoryType] = {}
            cls._valid_value_ids: Dict[int, FinalPretreatmentNCategoryType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["FinalPretreatmentNCategoryType"]:
        """
        Returns the FinalPretreatmentNCategoryType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["FinalPretreatmentNCategoryType"]:
        """
        Returns the FinalPretreatmentNCategoryType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["FinalPretreatmentNCategoryType"]:
        """
        Returns the FinalPretreatmentNCategoryType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """Returns the valid value ID for the N category."""
        return self._valid_value_id

    def get_description(self) -> str:
        """Returns the description for the N category."""
        return self._description
