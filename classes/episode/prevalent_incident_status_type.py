from enum import Enum


class PrevalentIncidentStatusType(Enum):
    """
    Enum for mapping symbolic values for FOBT prevalent/incident episode classification.

    Members:
        PREVALENT: Represents a prevalent episode.
        INCIDENT: Represents an incident episode.
    """

    PREVALENT = "prevalent"
    INCIDENT = "incident"

    @classmethod
    def from_description(cls, description: str) -> "PrevalentIncidentStatusType":
        """
        Returns the Enum member for a given description.

        Args:
            description (str): The description to check.

        Returns:
            PrevalentIncidentStatusType: The corresponding Enum member.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        for member in cls:
            if member.value == key:
                return member
        raise ValueError(f"Unknown FOBT episode status: '{description}'")
