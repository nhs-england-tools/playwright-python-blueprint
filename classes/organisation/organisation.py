class Organisation:
    """
    Class representing an organisation with a unique organisation ID.

    Methods:
        get_organisation_id() -> str:
            Returns the organisation's unique ID.
    """

    def __init__(self, organisation_id: str):
        """
        Initialize an Organisation instance.

        Args:
            organisation_id (str): The unique identifier for the organisation.
        """
        self.organisation_id = organisation_id

    def get_organisation_id(self) -> str:
        """
        Returns the organisation's unique ID.

        Returns:
            str: The organisation ID.
        """
        return self.organisation_id
