from enum import Enum
from typing import Optional, Dict


class ASAGradeType(Enum):
    """
    Enum representing ASA grades for colonoscopy assessment scenarios,
    with valid value IDs and descriptions.
    """

    IFIT = (17009, "I - Fit")
    II_RELEVANT_DISEASE = (17010, "II - Relevant disease")
    III_RESTRICTIVE_DISEASE = (17011, "III - Restrictive disease")
    IV_LIFE_THREATENING_DISEASE = (17012, "IV - Life threatening disease")
    V_MORIBUND = (17013, "V - Moribund")
    NOT_APPLICABLE = (17014, "Not Applicable")
    NOT_KNOWN = (17015, "Not Known")
    NULL = (None, "")

    def __init__(self, valid_value_id: Optional[int], description: str):
        self._valid_value_id: Optional[int] = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """Returns the valid value ID for the ASA grade."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the ASA grade."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for ASAGradeType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, ASAGradeType] = {}
            cls._lowercase_descriptions: Dict[str, ASAGradeType] = {}
            cls._valid_value_ids: Dict[Optional[int], ASAGradeType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["ASAGradeType"]:
        """
        Returns the ASAGradeType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["ASAGradeType"]:
        """
        Returns the ASAGradeType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: Optional[int]
    ) -> Optional["ASAGradeType"]:
        """
        Returns the ASAGradeType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_valid_value_id(self) -> Optional[int]:
        """
        Returns the valid value ID for the ASA grade.
        """
        return self._valid_value_id

    def get_description(self) -> str:
        """
        Returns the description for the ASA grade.
        """
        return self._description
