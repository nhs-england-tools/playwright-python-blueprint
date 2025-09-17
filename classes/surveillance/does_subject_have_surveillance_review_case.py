from enum import Enum


class DoesSubjectHaveSurveillanceReviewCase(Enum):
    """
    Enum for mapping binary criteria for the presence of a surveillance review case.
    """

    YES = "Yes"
    NO = "No"

    @classmethod
    def from_description(
        cls, description: str
    ) -> "DoesSubjectHaveSurveillanceReviewCase":
        """
        Returns the Enum member for a given description.

        Args:
            description (str): The description to check (e.g., "Yes" or "No").

        Returns:
            DoesSubjectHaveSurveillanceReviewCase: The corresponding Enum member.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().capitalize()
        for member in cls:
            if member.value == key:
                return member
        raise ValueError(f"Unknown surveillance review case presence: '{description}'")
