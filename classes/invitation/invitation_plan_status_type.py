from enum import Enum
from typing import Optional


class InvitationPlanStatusType(Enum):
    """
    Invitation Plan Status types, as defined in the VALID_VALUES table.
    """

    ACTIVE = (202404, "ACTIVE")
    TEMPORARY = (202403, "TEMPORARY")
    FINISHED = (202405, "FINISHED")

    def __init__(self, valid_value_id: int, allowed_value: str) -> None:
        self._valid_value_id = valid_value_id
        self._allowed_value = allowed_value

    @property
    def id(self) -> int:
        """
        Returns the valid value ID for the status.
        """
        return self._valid_value_id

    @property
    def allowed_value(self) -> str:
        """
        Returns the allowed value string for the status.
        """
        return self._allowed_value

    @classmethod
    def value_of(
        cls, plan_type_id: Optional[int]
    ) -> Optional["InvitationPlanStatusType"]:
        """
        Returns the InvitationPlanStatusType corresponding to the given ID.

        Args:
            plan_type_id (Optional[int]): The ID to look up.

        Returns:
            Optional[InvitationPlanStatusType]: The matching enum member, or None if not found.
        """
        if plan_type_id is None:
            return None
        for status in cls:
            if status.id == plan_type_id:
                return status
        return None
