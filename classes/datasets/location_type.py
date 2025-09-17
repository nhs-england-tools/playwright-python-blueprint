from enum import Enum
from typing import Optional, Dict


class LocationType(Enum):
    """
    Enum representing anatomical locations for datasets,
    with valid value IDs and descriptions.
    """

    ANUS = (17231, "Anus")
    RECTUM = (17232, "Rectum")
    RECTO_SIGMOID = (17243, "Recto/Sigmoid")  # Used in CADS
    SIGMOID_COLON = (17233, "Sigmoid Colon")
    DESCENDING_COLON = (17234, "Descending Colon")
    SPLENIC_FLEXURE = (17235, "Splenic Flexure")
    TRANSVERSE_COLON = (17236, "Transverse Colon")
    HEPATIC_FLEXURE = (17237, "Hepatic Flexure")
    ASCENDING_COLON = (17238, "Ascending Colon")
    CAECUM = (17239, "Caecum")
    ILEUM = (17240, "Ileum")
    ANASTOMOSIS = (17241, "Anastomosis")
    APPENDIX = (17242, "Appendix")
    LEFT_COLON = (17244, "Left colon")  # Used in investigation datasets, other findings
    ENTIRE_COLON = (
        17245,
        "Entire colon",
    )  # Used in investigation datasets, other findings
    RIGHT_COLON = (
        200619,
        "Right colon",
    )  # Used in investigation datasets, other findings
    PATCHY_AREAS = (
        200618,
        "Patchy areas",
    )  # Used in investigation datasets, other findings

    def __init__(self, valid_value_id: int, description: str):
        self._valid_value_id: int = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the location."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the location."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for LocationType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, LocationType] = {}
            cls._lowercase_descriptions: Dict[str, LocationType] = {}
            cls._valid_value_ids: Dict[int, LocationType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["LocationType"]:
        """
        Returns the LocationType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["LocationType"]:
        """
        Returns the LocationType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["LocationType"]:
        """
        Returns the LocationType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """Returns the valid value ID for the location."""
        return self._valid_value_id

    def get_description(self) -> str:
        """Returns the description for the location."""
        return self._description
