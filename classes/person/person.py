from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Person:
    """
    Represents a person with identifying and role-related attributes.

    Attributes:
        person_id (Optional[int]): Unique identifier for the person (PRS ID).
        surname (Optional[str]): The surname of the person.
        forenames (Optional[str]): The forenames of the person.
        registration_code (Optional[str]): The registration code of the person.
        role_id (Optional[int]): Role identifier (PIO ID). Used to hold one
            selected role for the person.
    """

    person_id: Optional[int] = field(default=None)
    surname: Optional[str] = field(default=None)
    forenames: Optional[str] = field(default=None)
    registration_code: Optional[str] = field(default=None)
    role_id: Optional[int] = field(default=None)

    @property
    def full_name(self) -> str:
        """
        Get the full name of the person.

        Returns:
            str: The concatenation of forenames and surname, or an empty string if missing.
        """
        parts = [self.forenames or "", self.surname or ""]
        return " ".join(p for p in parts if p).strip()

    def __str__(self) -> str:
        """
        Get a string representation of the person object.

        Returns:
            str: String with field values, similar to the Java `toString` implementation.
        """
        return (
            f"User [personId={self.person_id}, "
            f"surname={self.surname}, "
            f"forenames={self.forenames}, "
            f"registrationCode={self.registration_code}, "
            f"roleId={self.role_id}]"
        )
