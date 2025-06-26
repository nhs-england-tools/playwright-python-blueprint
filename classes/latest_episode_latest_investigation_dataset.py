class LatestEpisodeLatestInvestigationDataset:
    """
    Utility class for mapping descriptive investigation filter criteria to internal constants.

    This class is used to drive investigation dataset filtering in the latest episode.

    Members:
        NONE: No investigation dataset.
        COLONOSCOPY_NEW: New colonoscopy dataset.
        LIMITED_COLONOSCOPY_NEW: New limited colonoscopy dataset.
        FLEXIBLE_SIGMOIDOSCOPY_NEW: New flexible sigmoidoscopy dataset.
        CT_COLONOGRAPHY_NEW: New CT colonography dataset.
        ENDOSCOPY_INCOMPLETE: Incomplete endoscopy dataset.
        RADIOLOGY_INCOMPLETE: Incomplete radiology dataset.

    Methods:
        from_description(description: str) -> str:
            Returns the internal constant for a given description.
            Raises ValueError if the description is not recognized.
    """

    NONE = "none"
    COLONOSCOPY_NEW = "colonoscopy_new"
    LIMITED_COLONOSCOPY_NEW = "limited_colonoscopy_new"
    FLEXIBLE_SIGMOIDOSCOPY_NEW = "flexible_sigmoidoscopy_new"
    CT_COLONOGRAPHY_NEW = "ct_colonography_new"
    ENDOSCOPY_INCOMPLETE = "endoscopy_incomplete"
    RADIOLOGY_INCOMPLETE = "radiology_incomplete"

    _valid_values = {
        NONE,
        COLONOSCOPY_NEW,
        LIMITED_COLONOSCOPY_NEW,
        FLEXIBLE_SIGMOIDOSCOPY_NEW,
        CT_COLONOGRAPHY_NEW,
        ENDOSCOPY_INCOMPLETE,
        RADIOLOGY_INCOMPLETE,
    }

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the internal constant for a given description.

        Args:
            description (str): The description to check.

        Returns:
            str: The internal constant matching the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._valid_values:
            raise ValueError(f"Unknown investigation dataset filter: '{description}'")
        return key
