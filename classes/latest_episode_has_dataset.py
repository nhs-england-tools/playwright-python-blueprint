class LatestEpisodeHasDataset:
    """
    Utility class for interpreting the presence and completion status of datasets in the latest episode.

    This class provides:
        - Logical flags for "no", "yes_incomplete", "yes_complete", and "past" to indicate dataset status.
        - A method to convert a description to a valid flag.

    Members:
        NO: No dataset present.
        YES_INCOMPLETE: Dataset present but incomplete.
        YES_COMPLETE: Dataset present and complete.
        PAST: Dataset present in a past episode.

    Methods:
        from_description(description: str) -> str:
            Returns the logical flag for a given description.
            Raises ValueError if the description is not recognized.
    """

    NO = "no"
    YES_INCOMPLETE = "yes_incomplete"
    YES_COMPLETE = "yes_complete"
    PAST = "past"

    _valid_values = {NO, YES_INCOMPLETE, YES_COMPLETE, PAST}

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the logical flag for a given description.

        Args:
            description (str): The description to check (e.g., "no", "yes_incomplete", "yes_complete", "past").

        Returns:
            str: The logical flag matching the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._valid_values:
            raise ValueError(f"Unknown dataset status: '{description}'")
        return key
