from enum import Enum


class HasGPPractice(Enum):
    """
    Enum representing whether a subject has a GP practice and its status.

    Members:
        NO: No GP practice.
        YES_ACTIVE: Has an active GP practice.
        YES_INACTIVE: Has an inactive GP practice.

    Methods:
        by_description(description: str) -> Optional[HasGPPractice]:
            Returns the enum member matching the given description, or None if not found.
        get_description() -> str:
            Returns the string description of the enum member.
    """

    NO = "no"
    YES_ACTIVE = "yes - active"
    YES_INACTIVE = "yes - inactive"

    @classmethod
    def by_description(cls, description: str):
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[HasGPPractice]: The matching enum member, or None if not found.
        """
        for member in cls:
            if member.value == description:
                return member
        return None

    def get_description(self):
        """
        Returns the string description of the enum member.

        Returns:
            str: The description value.
        """
        return self.value
