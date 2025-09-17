from enum import Enum
from typing import Optional, Dict


class EpisodeSubType(Enum):
    """
    Enum representing sub-types of an episode in the BCSS system.

    Each sub-type has a unique valid value ID and a description.
    Provides utility methods for lookup by description (case-sensitive and insensitive)
    and by valid value ID.
    """

    LATE_RESPONDER = (200500, "Late Responder")
    OPT_IN = (200503, "Opt-in")
    OVER_AGE = (200502, "Over Age")
    ROUTINE = (200501, "Routine")
    SELF_REFER = (205003, "Self-Refer")

    def __init__(self, valid_value_id: int, description: str):
        """
        Initialize an EpisodeSubType enum member.

        Args:
            valid_value_id (int): The unique identifier for the sub-type.
            description (str): The human-readable description of the sub-type.
        """
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique valid value ID for this sub-type.

        Returns:
            int: The valid value ID.
        """
        return self._valid_value_id

    @property
    def description(self) -> str:
        """
        Returns the description for this sub-type.

        Returns:
            str: The description.
        """
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for EpisodeSubType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, EpisodeSubType] = {}
            cls._lowercase_descriptions: Dict[str, EpisodeSubType] = {}
            cls._valid_value_ids: Dict[int, EpisodeSubType] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["EpisodeSubType"]:
        """
        Lookup an EpisodeSubType by its exact description.

        Args:
            description (str): The description to look up.

        Returns:
            Optional[EpisodeSubType]: The matching enum member, or None if not found.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["EpisodeSubType"]:
        """
        Lookup an EpisodeSubType by its description, case-insensitive.

        Args:
            description (str): The description to look up.

        Returns:
            Optional[EpisodeSubType]: The matching enum member, or None if not found.
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["EpisodeSubType"]:
        """
        Lookup an EpisodeSubType by its valid value ID.

        Args:
            valid_value_id (int): The valid value ID to look up.

        Returns:
            Optional[EpisodeSubType]: The matching enum member, or None if not found.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """
        Returns the valid value ID for this sub-type.

        Returns:
            int: The valid value ID.
        """
        return self._valid_value_id

    def get_description(self) -> str:
        """
        Returns the description for this sub-type.

        Returns:
            str: The description.
        """
        return self._description
