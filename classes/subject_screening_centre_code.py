from enum import Enum


class SubjectScreeningCentreCode(Enum):
    """
    Enum representing subject screening centre code types.

    Members:
        NONE: No screening centre.
        NULL: Null value for subject selection criteria.
        NOT_NULL: Not Null value for subject selection criteria.
        USER_SC: User's screening centre (abbreviated).
        USER_SCREENING_CENTRE: User's screening centre (full).
        USER_ORGANISATION: User's organisation.

    Methods:
        description: Returns the string description of the enum member.
        by_description(description: str) -> Optional[SubjectScreeningCentreCode]:
            Returns the enum member matching the given description, or None if not found.
        by_description_case_insensitive(description: str) -> Optional[SubjectScreeningCentreCode]:
            Returns the enum member matching the given description (case-insensitive), or None if not found.
    """

    NONE = "None"
    NULL = "Null"
    NOT_NULL = "Not null"
    USER_SC = "User's SC"
    USER_SCREENING_CENTRE = "User's screening centre"
    USER_ORGANISATION = "User's organisation"

    @property
    def description(self):
        """
        Returns the string description of the enum member.

        Returns:
            str: The description value.
        """
        return self.value

    @staticmethod
    def by_description(description: str):
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SubjectScreeningCentreCode]: The matching enum member, or None if not found.
        """
        for item in SubjectScreeningCentreCode:
            if item.description == description:
                return item
        return None  # or raise an exception

    @staticmethod
    def by_description_case_insensitive(description: str):
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            description (str): The description to search for.

        Returns:
            Optional[SubjectScreeningCentreCode]: The matching enum member, or None if not found.
        """
        description_lower = description.lower()
        for item in SubjectScreeningCentreCode:
            if item.description.lower() == description_lower:
                return item
        return None  # or raise an exception
