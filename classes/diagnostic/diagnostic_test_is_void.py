from enum import Enum


class DiagnosticTestIsVoid(Enum):
    """
    Enum for mapping descriptive yes/no flags to test void state checks.
    """

    YES = "Yes"
    NO = "No"

    @classmethod
    def from_description(cls, description: str) -> "DiagnosticTestIsVoid":
        """
        Returns the Enum member for a given description.

        Args:
            description (str): The description to check (e.g., "Yes" or "No").

        Returns:
            DiagnosticTestIsVoid: The corresponding Enum member.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        for member in cls:
            if member.value == key:
                return member
        raise ValueError(f"Unknown test void flag: '{description}'")
