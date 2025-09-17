from enum import Enum
from typing import Optional, Dict


class YesNo(Enum):
    """
    Enum representing Yes/No values with descriptions.
    """

    NO = "No"
    YES = "Yes"

    def __init__(self, description: str):
        self._description: str = description

    @property
    def description(self) -> str:
        """Returns the description for the Yes/No value."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for YesNo enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, YesNo] = {}
            cls._lowercase_descriptions: Dict[str, YesNo] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["YesNo"]:
        """
        Returns the YesNo value matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(cls, description: str) -> Optional["YesNo"]:
        """
        Returns the YesNo value matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())
