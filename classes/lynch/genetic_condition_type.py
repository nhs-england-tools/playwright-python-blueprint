from enum import Enum
from typing import Optional


class GeneticConditionType(Enum):
    """
    Enum representing genetic condition types with valid value ID, description, and lower age.
    Provides lookup by description and valid value ID.
    """

    EPCAM = (307070, "EPCAM", 25)
    MLH1 = (306443, "MLH1", 25)
    MSH2 = (306444, "MSH2", 25)
    MSH6 = (306445, "MSH6", 35)
    PMS2 = (306446, "PMS2", 35)

    def __init__(self, valid_value_id: int, description: str, lower_age: int):
        self._valid_value_id = valid_value_id
        self._description = description
        self._lower_age = lower_age

    @property
    def valid_value_id(self) -> int:
        """Return the valid value ID."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Return the description."""
        return self._description

    @property
    def lower_age(self) -> int:
        """Return the lower age."""
        return self._lower_age

    @classmethod
    def by_description(cls, description: str) -> Optional["GeneticConditionType"]:
        """Return the GeneticConditionType instance for the given description."""
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["GeneticConditionType"]:
        """Return the GeneticConditionType instance for the given valid value ID."""
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
