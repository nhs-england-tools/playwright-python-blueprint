from enum import Enum
from typing import Optional


class GenderType(Enum):
    """
    Enum representing gender types for a subject.

    Members:
        MALE: Male gender (valid_value_id=130, redefined_value=1, allowed_value="M")
        FEMALE: Female gender (valid_value_id=131, redefined_value=2, allowed_value="F")
        INDETERMINATE: Indeterminate gender (valid_value_id=132, redefined_value=9, allowed_value="I")
        NOT_KNOWN: Not known gender (valid_value_id=160, redefined_value=0, allowed_value="U")
    """

    MALE = (130, 1, "M")
    FEMALE = (131, 2, "F")
    INDETERMINATE = (132, 9, "I")
    NOT_KNOWN = (160, 0, "U")

    def __init__(self, valid_value_id: int, redefined_value: int, allowed_value: str):
        """
        Initialize a GenderType enum member.

        Args:
            valid_value_id (int): The unique identifier for the gender type.
            redefined_value (int): The redefined value for the gender type.
            allowed_value (str): The string representation of the gender type.
        """
        self._valid_value_id = valid_value_id
        self._redefined_value = redefined_value
        self._allowed_value = allowed_value

    @property
    def valid_value_id(self) -> int:
        """
        Returns the unique identifier for the gender type.

        Returns:
            int: The valid value ID.
        """
        return self._valid_value_id

    @property
    def redefined_value(self) -> int:
        """
        Returns the redefined value for the gender type.

        Returns:
            int: The redefined value.
        """
        return self._redefined_value

    @property
    def allowed_value(self) -> str:
        """
        Returns the string representation of the gender type.

        Returns:
            str: The allowed value.
        """
        return self._allowed_value

    @classmethod
    def by_valid_value_id(cls, id_: int) -> Optional["GenderType"]:
        """
        Returns the GenderType enum member matching the given valid value ID.

        Args:
            id_ (int): The valid value ID to search for.

        Returns:
            Optional[GenderType]: The matching enum member, or None if not found.
        """
        return next((item for item in cls if item.valid_value_id == id_), None)

    @classmethod
    def by_redefined_value(cls, redefined_value: int) -> Optional["GenderType"]:
        """
        Returns the GenderType enum member matching the given redefined value.

        Args:
            redefined_value (int): The redefined value to search for.

        Returns:
            Optional[GenderType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.redefined_value == redefined_value), None
        )

    @classmethod
    def by_allowed_value(cls, allowed_value: str) -> Optional["GenderType"]:
        """
        Returns the GenderType enum member matching the given allowed value.

        Args:
            allowed_value (str): The allowed value to search for.

        Returns:
            Optional[GenderType]: The matching enum member, or None if not found.
        """
        return next(
            (item for item in cls if item.allowed_value == allowed_value), None
        )
