from enum import Enum
from typing import Optional


class AddressType(Enum):
    """
    Enum representing the type of address for a subject.

    Attributes:
        MAIN_REGISTERED_ADDRESS: Represents the main registered address (code "H").
        TEMPORARY_ADDRESS: Represents a temporary address (code "T").
    """

    MAIN_REGISTERED_ADDRESS = (13042, "H")
    TEMPORARY_ADDRESS = (13043, "T")

    def __init__(self, valid_value_id: int, allowed_value: str):
        """
        Initialize an AddressType enum member.

        Args:
            valid_value_id (int): The unique identifier for the address type.
            allowed_value (str): The string representation of the address type.
        """
        self._valid_value_id = valid_value_id
        self._allowed_value = allowed_value

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique identifier for the address type.

        Returns:
            int: The valid value ID.
        """
        return self._valid_value_id

    @property
    def allowed_value(self) -> str:
        """
        Returns the string representation of the address type.

        Returns:
            str: The allowed value.
        """
        return self._allowed_value

    @classmethod
    def by_valid_value_id(cls, address_type_id: int) -> Optional["AddressType"]:
        """
        Returns the AddressType enum member matching the given valid value ID.

        Args:
            address_type_id (int): The valid value ID to search for.

        Returns:
            Optional[AddressType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.valid_value_id == address_type_id), None
        )
