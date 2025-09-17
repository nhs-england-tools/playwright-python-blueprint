from enum import Enum


class InvitedSinceAgeExtension(Enum):
    """
    Enum for mapping subject invitation criteria based on age extension presence.

    Members:
        YES: Indicates the subject was invited since the age extension.
        NO: Indicates the subject was not invited since the age extension.
    """

    YES = "Yes"
    NO = "No"

    @classmethod
    def from_description(cls, description: str) -> "InvitedSinceAgeExtension":
        """
        Returns the Enum member for a given description.

        Args:
            description (str): The description to check (e.g., "Yes" or "No").

        Returns:
            InvitedSinceAgeExtension: The corresponding Enum member.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().capitalize()
        for member in cls:
            if member.value == key:
                return member
        raise ValueError(f"Invalid invited-since-age-extension flag: '{description}'")
