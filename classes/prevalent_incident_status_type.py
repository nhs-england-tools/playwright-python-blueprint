class PrevalentIncidentStatusType:
    """
    Utility class for mapping symbolic values for FOBT prevalent/incident episode classification.

    Members:
        PREVALENT: Represents a prevalent episode.
        INCIDENT: Represents an incident episode.

    Methods:
        from_description(description: str) -> str:
            Returns the symbolic value ("prevalent" or "incident") for a given description.
            Raises ValueError if the description is not recognized.
    """

    PREVALENT = "prevalent"
    INCIDENT = "incident"

    _valid_values = {PREVALENT, INCIDENT}

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the symbolic value ("prevalent" or "incident") for a given description.

        Args:
            description (str): The description to check.

        Returns:
            str: The symbolic value ("prevalent" or "incident").

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._valid_values:
            raise ValueError(f"Unknown FOBT episode status: '{description}'")
        return key
