from enum import Enum
from typing import Optional, Dict


class YesNoType(Enum):
    """
    Enum representing Yes/No values for investigation datasets, with valid value IDs and descriptions.
    """

    YES = (17058, "Yes")
    NO = (17059, "No")
    NULL = (None, "Null")

    def __init__(self, valid_value_id: Optional[int], description: str):
        self._valid_value_id: Optional[int] = valid_value_id
        self._description: str = description

    @property
    def valid_value_id(self) -> Optional[int]:
        """Returns the valid value ID for the Yes/No value."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the Yes/No value."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for YesNoType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, YesNoType] = {}
            cls._lowercase_descriptions: Dict[str, YesNoType] = {}
            cls._valid_value_ids: Dict[Optional[int], YesNoType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["YesNoType"]:
        """
        Returns the YesNoType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(cls, description: str) -> Optional["YesNoType"]:
        """
        Returns the YesNoType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(cls, valid_value_id: Optional[int]) -> Optional["YesNoType"]:
        """
        Returns the YesNoType matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> Optional[int]:
        """Returns the valid value ID for the Yes/No value."""
        return self._valid_value_id

    def get_description(self) -> str:
        """Returns the description for the Yes/No value."""
        return self._description
