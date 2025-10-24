from dataclasses import dataclass
from typing import Optional
from classes.subject.gender_type import GenderType


@dataclass
class Person:
    """
    Represents a person with name, title, previous surname, other forenames, and gender.
    Provides methods to get full name and string representation.
    """

    surname: Optional[str] = None
    forename: Optional[str] = None
    title: Optional[str] = None
    other_forenames: Optional[str] = None
    previous_surname: Optional[str] = None
    gender: Optional[GenderType] = None

    def get_full_name(self) -> str:
        """
        Returns the full name of the person.
        """
        return f"{self.title or ''} {self.forename or ''} {self.surname or ''}".strip()

    def __str__(self) -> str:
        """
        Returns a string representation of the person.
        """
        return f"{self.title or ''} {self.forename or ''} {self.surname or ''} (gender={self.gender})".strip()
