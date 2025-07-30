from enum import Enum
from typing import Optional, Dict


class CancerTreatmentIntent(Enum):
    """
    Enum representing types of cancer treatment intent with associated valid value IDs and descriptions.
    Provides utility methods to retrieve enum instances by description or ID.
    """

    CURATIVE = (17370, "Curative")
    PALLIATIVE = (17371, "Palliative")
    UNCERTAIN = (17372, "Uncertain")
    NOT_KNOWN = (17373, "Not Known")

    def __init__(self, valid_value_id: int, description: str):
        self._valid_value_id = valid_value_id
        self._description = description

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
        Initializes internal lookup maps for CanterTreatmentIntent enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_descriptions"):
            cls._descriptions: Dict[str, CancerTreatmentIntent] = {}
            cls._lowercase_descriptions: Dict[str, CancerTreatmentIntent] = {}
            cls._valid_value_ids: Dict[int, CancerTreatmentIntent] = {}
            for item in cls:
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._valid_value_ids[item.valid_value_id] = item

    @classmethod
    def by_description(cls, description: str) -> Optional["CancerTreatmentIntent"]:
        """
        Returns the CancerTreatmentIntent matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["CancerTreatmentIntent"]:
        """
        Returns the CancerTreatmentIntent matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_valid_value_id(
        cls, valid_value_id: int
    ) -> Optional["CancerTreatmentIntent"]:
        """
        Returns the CancerTreatmentIntent matching the given valid value ID.
        """
        cls._build_maps()
        return cls._valid_value_ids.get(valid_value_id)

    def get_id(self) -> int:
        """Returns the valid value ID for the CancerTreatmentIntent given."""
        return self._valid_value_id

    def get_description(self) -> str:
        """Returns the description for the CancerTreatmentIntent given."""
        return self._description
