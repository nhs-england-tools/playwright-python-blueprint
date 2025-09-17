from enum import Enum
from typing import Optional


class WhichDiagnosticTest(Enum):
    """
    Enum representing which diagnostic test to select, with description and test number.
    Provides utility methods for lookup by description (case-sensitive and insensitive).
    Conventions:
        - test_number > 0: Refers to an explicit test index within the latest episode
        (e.g., test 1, test 2, ...).
        - test_number == 0: Indicates a selection rule or condition rather than a
        fixed test index (e.g., "any test", "latest test", "earliest not-void test").
    """

    ANY_TEST_IN_ANY_EPISODE = ("any test in any episode", 0)
    ANY_TEST_IN_LATEST_EPISODE = ("any test in latest episode", 0)
    EARLIER_TEST_IN_LATEST_EPISODE = ("earlier test in latest episode", 0)
    LATER_TEST_IN_LATEST_EPISODE = ("later test in latest episode", 0)
    LATEST_EPISODE_TEST_1 = ("latest episode test 1", 1)
    LATEST_EPISODE_TEST_2 = ("latest episode test 2", 2)
    LATEST_EPISODE_TEST_3 = ("latest episode test 3", 3)
    LATEST_EPISODE_TEST_4 = ("latest episode test 4", 4)
    LATEST_EPISODE_TEST_5 = ("latest episode test 5", 5)
    LATEST_EPISODE_TEST_6 = ("latest episode test 6", 6)
    LATEST_EPISODE_TEST_7 = ("latest episode test 7", 7)
    LATEST_EPISODE_TEST_8 = ("latest episode test 8", 8)
    LATEST_EPISODE_TEST_9 = ("latest episode test 9", 9)
    LATEST_EPISODE_TEST_10 = ("latest episode test 10", 10)
    LATEST_NOT_VOID_TEST_IN_LATEST_EPISODE = (
        "latest not-void test in latest episode",
        0,
    )
    LATEST_TEST_IN_LATEST_EPISODE = ("latest test in latest episode", 0)
    EARLIEST_NOT_VOID_TEST_IN_LATEST_EPISODE = (
        "earliest not-void test in latest episode",
        0,
    )
    ONLY_NOT_VOID_TEST_IN_LATEST_EPISODE = ("only not-void test in latest episode", 0)
    ONLY_TEST_IN_LATEST_EPISODE = ("only test in latest episode", 0)

    def __init__(self, description: str, test_number: int) -> None:
        self._description = description
        self._test_number = test_number

    @property
    def description(self) -> str:
        """
        Returns the description for the diagnostic test selection.
        """
        return self._description

    @property
    def test_number(self) -> int:
        """
        Returns the test number for the diagnostic test selection.
        """
        return self._test_number

    @classmethod
    def by_description(cls, description: str) -> Optional["WhichDiagnosticTest"]:
        """
        Returns the enum member matching the given description (case-sensitive).
        """
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["WhichDiagnosticTest"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None
