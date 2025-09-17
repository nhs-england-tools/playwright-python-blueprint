from enum import Enum
from typing import Optional


class IntendedExtentType(Enum):
    """
    Enum for representing intended extent types.
    """

    ANASTOMOSIS = (17241, "Anastomosis")
    ANUS = (17231, "Anus")
    APPENDIX = (17242, "Appendix")
    ASCENDING_COLON = (17238, "Ascending Colon")
    CAECUM = (17239, "Caecum")
    DESCENDING_COLON = (17234, "Descending Colon")
    DISTAL_SIGMOID = (17965, "Distal sigmoid")  # Legacy value
    ENTIRE_COLON = (17245, "Entire colon")  # Legacy value
    HEPATIC_FLEXURE = (17237, "Hepatic Flexure")
    ILEUM = (17240, "Ileum")
    LEFT_COLON = (17244, "Left colon")  # Legacy value
    MID_SIGMOID = (17966, "Mid sigmoid")  # Legacy value
    PROXIMAL_SIGMOID = (17967, "Proximal sigmoid")  # Legacy value
    RECTO_SIGMOID = (17243, "Recto/Sigmoid")  # Legacy value
    RECTOSIGMOID_JUNCTION = (17964, "Rectosigmoid junction")  # Legacy value
    RECTUM = (17232, "Rectum")
    SIGMOID_COLON = (17233, "Sigmoid Colon")
    SPLENIC_FLEXURE = (17235, "Splenic Flexure")
    TRANSVERSE_COLON = (17236, "Transverse Colon")
    NULL = (None, "NULL")
    NOT_NULL = (None, "NOT NULL")

    def __init__(self, valid_value_id: Optional[int], description: str):
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """Returns the valid value ID."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description."""
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["IntendedExtentType"]:
        """
        Returns the IntendedExtentType member matching the given description.
        """
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["IntendedExtentType"]:
        """
        Returns the IntendedExtentType member matching the given description (case insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: Optional[int]
    ) -> Optional["IntendedExtentType"]:
        """
        Returns the IntendedExtentType member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
