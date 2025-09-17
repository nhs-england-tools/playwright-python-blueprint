from enum import Enum


class LatestEpisodeHasDataset(Enum):
    """
    Enum for interpreting the presence and completion status of datasets in the latest episode.

    Members:
        NO: No dataset present.
        YES_INCOMPLETE: Dataset present but incomplete.
        YES_COMPLETE: Dataset present and complete.
        PAST: Dataset present in a past episode.
    """

    NO = "No"
    YES_INCOMPLETE = "Yes - incomplete"
    YES_COMPLETE = "Yes - complete"
    PAST = "Past"

    @classmethod
    def from_description(cls, description: str) -> "LatestEpisodeHasDataset":
        """
        Returns the Enum member for a given description.

        Args:
            description (str): The description to check.

        Returns:
            LatestEpisodeHasDataset: The corresponding Enum member.

        Raises:
            ValueError: If the description is not recognized.
        """
        normalized = description.strip().lower()
        for member in cls:
            if member.value.lower() == normalized:
                return member
        raise ValueError(f"Unknown dataset status: '{description}'")
