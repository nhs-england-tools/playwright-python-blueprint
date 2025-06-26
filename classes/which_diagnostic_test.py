class WhichDiagnosticTest:
    """
    Maps descriptive diagnostic test selection types to internal constants.
    Used to determine join and filter behavior in the query builder.

    Members:
        ANY_TEST_IN_ANY_EPISODE: Any test in any episode.
        ANY_TEST_IN_LATEST_EPISODE: Any test in the latest episode.
        ONLY_TEST_IN_LATEST_EPISODE: Only test in the latest episode.
        ONLY_NOT_VOID_TEST_IN_LATEST_EPISODE: Only not void test in the latest episode.
        LATEST_TEST_IN_LATEST_EPISODE: Latest test in the latest episode.
        LATEST_NOT_VOID_TEST_IN_LATEST_EPISODE: Latest not void test in the latest episode.
        EARLIEST_NOT_VOID_TEST_IN_LATEST_EPISODE: Earliest not void test in the latest episode.
        EARLIER_TEST_IN_LATEST_EPISODE: Earlier test in the latest episode.
        LATER_TEST_IN_LATEST_EPISODE: Later test in the latest episode.

    Methods:
        from_description(description: str) -> str:
            Returns the internal constant for a given description.
            Raises ValueError if the description is not recognized.
    """

    ANY_TEST_IN_ANY_EPISODE = "any_test_in_any_episode"
    ANY_TEST_IN_LATEST_EPISODE = "any_test_in_latest_episode"
    ONLY_TEST_IN_LATEST_EPISODE = "only_test_in_latest_episode"
    ONLY_NOT_VOID_TEST_IN_LATEST_EPISODE = "only_not_void_test_in_latest_episode"
    LATEST_TEST_IN_LATEST_EPISODE = "latest_test_in_latest_episode"
    LATEST_NOT_VOID_TEST_IN_LATEST_EPISODE = "latest_not_void_test_in_latest_episode"
    EARLIEST_NOT_VOID_TEST_IN_LATEST_EPISODE = (
        "earliest_not_void_test_in_latest_episode"
    )
    EARLIER_TEST_IN_LATEST_EPISODE = "earlier_test_in_latest_episode"
    LATER_TEST_IN_LATEST_EPISODE = "later_test_in_latest_episode"

    _valid_values = {
        ANY_TEST_IN_ANY_EPISODE,
        ANY_TEST_IN_LATEST_EPISODE,
        ONLY_TEST_IN_LATEST_EPISODE,
        ONLY_NOT_VOID_TEST_IN_LATEST_EPISODE,
        LATEST_TEST_IN_LATEST_EPISODE,
        LATEST_NOT_VOID_TEST_IN_LATEST_EPISODE,
        EARLIEST_NOT_VOID_TEST_IN_LATEST_EPISODE,
        EARLIER_TEST_IN_LATEST_EPISODE,
        LATER_TEST_IN_LATEST_EPISODE,
    }

    @classmethod
    def from_description(cls, description: str) -> str:
        """
        Returns the internal constant for a given description.

        Args:
            description (str): The description to look up.

        Returns:
            str: The internal constant matching the description.

        Raises:
            ValueError: If the description is not recognized.
        """
        key = description.strip().lower()
        if key not in cls._valid_values:
            raise ValueError(f"Unknown diagnostic test selection: '{description}'")
        return key
