from enum import Enum
from typing import Optional


class AddressContactType(Enum):
    """
    Enum representing the type of address contact for a subject.

    Attributes:
        WORK: Represents a work address contact type.
        HOME: Represents a home address contact type.
    """

    WORK = (13056, "WORK")
    HOME = (13057, "HOME")

    def __init__(self, valid_value_id: int, allowed_value: str):
        """
        Initialize an AddressContactType enum member.

        Args:
            valid_value_id (int): The unique identifier for the address contact type.
            allowed_value (str): The string representation of the address contact type.
        """
        self._valid_value_id = valid_value_id
        self._allowed_value = allowed_value

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique identifier for the address contact type.

        Returns:
            int: The valid value ID.
        """
        return self._valid_value_id

    @property
    def allowed_value(self) -> str:
        """
        Returns the string representation of the address contact type.

        Returns:
            str: The allowed value.
        """
        return self._allowed_value

    @classmethod
    def by_valid_value_id(
        cls, address_contact_type_id: int
    ) -> Optional["AddressContactType"]:
        """
        Returns the AddressContactType enum member matching the given valid value ID.

        Args:
            address_contact_type_id (int): The valid value ID to search for.

        Returns:
            Optional[AddressContactType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.valid_value_id == address_contact_type_id),
            None,
        )
