from enum import Enum
from typing import Optional, Dict


class RecallEpisodeType(Enum):
    """
    Enum representing recall episode types with valid value IDs and descriptions.
    """

    ADENOMA_SURVEILLANCE_HIGH_RISK = (203149, "Adenoma Surveillance - High risk")
    ADENOMA_SURVEILLANCE_INTERMEDIATE_RISK = (
        203148,
        "Adenoma Surveillance - Intermediate risk",
    )
    BOWEL_SCOPE_SCREENING = (203164, "Bowel Scope Screening")
    FOBT_SCREENING = (203147, "FOBT Screening")
    SURVEILLANCE_LNPCP = (305610, "Surveillance - LNPCP")
    SURVEILLANCE_HIGH_RISK_FINDINGS = (305611, "Surveillance - High-risk findings")
    LYNCH_SURVEILLANCE = (305683, "Lynch Surveillance")
    NULL = (None, "Null")

    def __init__(self, valid_value_id: Optional[int], description: str):
        self._valid_value_id: Optional[int] = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """Returns the valid value ID for the recall episode type."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the recall episode type."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for RecallEpisodeType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, RecallEpisodeType] = {}
            cls._lowercase_descriptions: Dict[str, RecallEpisodeType] = {}
            cls._valid_value_ids: Dict[Optional[int], RecallEpisodeType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["RecallEpisodeType"]:
        """
        Returns the RecallEpisodeType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["RecallEpisodeType"]:
        """
        Returns the RecallEpisodeType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: Optional[int]
    ) -> Optional["RecallEpisodeType"]:
        """
        Returns the RecallEpisodeType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> Optional[int]:
        """
        Returns the valid value ID for the recall episode type.
        """
        return self._valid_value_id

    def get_description(self) -> str:
        """
        Returns the description for the recall episode type.
        """
        return self._description
