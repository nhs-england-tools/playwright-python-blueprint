from enum import Enum
from typing import Optional, Dict


class FinalPretreatmentTCategoryType(Enum):
    """
    Enum representing final pretreatment T categories for cancer audit datasets,
    with valid value IDs and descriptions.
    """

    CTX = (17356, "Primary tumour cannot be assessed (cTX)")
    CT0 = (202203, "No evidence of primary tumour (cT0)")
    CT1 = (17357, "Tumour invades submucosa (cT1)")
    CT2 = (17358, "Tumour invades muscularis propria (cT2)")
    CT3 = (
        17359,
        "Tumour invades through muscularis propria into subserosa or into non-peritonealized pericolic or peri-rectal tissues (cT3)",
    )
    CT4 = (
        17360,
        "Tumour directly invades other organs or structures and/or perforates visceral peritoneum (cT4)",
    )
    NOT_REPORTED = (202140, "Not Reported")

    def __init__(self, valid_value_id: int, description: str):
        self._valid_value_id: int = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the T category."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the T category."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for FinalPretreatmentTCategoryType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, FinalPretreatmentTCategoryType] = {}
            cls._lowercase_descriptions: Dict[str, FinalPretreatmentTCategoryType] = {}
            cls._valid_value_ids: Dict[int, FinalPretreatmentTCategoryType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(
        cls, description: str
    ) -> Optional["FinalPretreatmentTCategoryType"]:
        """
        Returns the FinalPretreatmentTCategoryType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["FinalPretreatmentTCategoryType"]:
        """
        Returns the FinalPretreatmentTCategoryType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["FinalPretreatmentTCategoryType"]:
        """
        Returns the FinalPretreatmentTCategoryType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """Returns the valid value ID for the T category."""
        return self._valid_value_id

    def get_description(self) -> str:
        """Returns the description for the T category."""
        return self._description
