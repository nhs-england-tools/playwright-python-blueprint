from typing import Optional
from classes.organisation_complex import Organisation
import pandas as pd


class User:
    """
    Class representing a user in the system.

    Attributes:
        user_id (Optional[int]): The unique identifier for the user.
        role_id (Optional[int]): The role identifier for the user.
        pio_id (Optional[int]): The PIO identifier for the user.
        organisation (Optional[Organisation]): The organisation associated with the user.

    Methods:
        __init__: Initializes a User instance.
        user_id: Gets or sets the user ID.
        role_id: Gets or sets the role ID.
        pio_id: Gets or sets the PIO ID.
        organisation: Gets or sets the organisation.
        __str__: Returns a string representation of the User.
    """

    def __init__(
        self,
        user_id: Optional[int] = None,
        role_id: Optional[int] = None,
        pio_id: Optional[int] = None,
        organisation: Optional[Organisation] = None,
    ):
        """
        Initialize a User instance.

        Args:
            user_id (Optional[int]): The unique identifier for the user.
            role_id (Optional[int]): The role identifier for the user.
            pio_id (Optional[int]): The PIO identifier for the user.
            organisation (Optional[Organisation]): The organisation associated with the user.
        """
        self._user_id = user_id
        self._role_id = role_id
        self._pio_id = pio_id
        self._organisation = organisation

    @property
    def user_id(self) -> Optional[int]:
        """
        Gets the user ID.

        Returns:
            Optional[int]: The user ID.
        """
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """
        Sets the user ID.

        Args:
            value (int): The user ID to set.
        """
        self._user_id = value

    @property
    def role_id(self) -> Optional[int]:
        """
        Gets the role ID.

        Returns:
            Optional[int]: The role ID.
        """
        return self._role_id

    @role_id.setter
    def role_id(self, value: int) -> None:
        """
        Sets the role ID.

        Args:
            value (int): The role ID to set.
        """
        self._role_id = value

    @property
    def pio_id(self) -> Optional[int]:
        """
        Gets the PIO ID.

        Returns:
            Optional[int]: The PIO ID.
        """
        return self._pio_id

    @pio_id.setter
    def pio_id(self, value: int) -> None:
        """
        Sets the PIO ID.

        Args:
            value (int): The PIO ID to set.
        """
        self._pio_id = value

    @property
    def organisation(self) -> Optional[Organisation]:
        """
        Gets the organisation.

        Returns:
            Optional[Organisation]: The organisation associated with the user.
        """
        return self._organisation

    @organisation.setter
    def organisation(self, value: Organisation) -> None:
        """
        Sets the organisation.

        Args:
            value (Organisation): The organisation to set.
        """
        self._organisation = value

    def __str__(self) -> str:
        """
        Returns a string representation of the User.

        Returns:
            str: The string representation of the user.
        """
        org_id = self.organisation.id if self.organisation else "None"
        return f"User [userId={self.user_id}, orgId={org_id}, roleId={self.role_id}]"

    def from_dataframe_row(self, row) -> "User":
        """
        Creates a User object from a pandas DataFrame row containing user query results.

        Args:
            row (pd.Series): A row from a pandas DataFrame with columns:
                - pio_id
                - org_id
                - role_id
                - org_code

        Returns:
            User: The constructed User object.
        """
        organisation = (
            Organisation(new_id=row["org_id"], new_code=row["org_code"])
            if "org_id" in row and "org_code" in row
            else None
        )

        return User(
            user_id=row["pio_id"],
            role_id=row["role_id"],
            pio_id=row["pio_id"],
            organisation=organisation,
        )
