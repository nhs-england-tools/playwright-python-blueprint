from enum import Enum
from typing import Optional


class PersonSelectionCriteriaKey(Enum):
    """
    Enum of person selection criteria keys with associated string descriptions.
    Provides lookup methods to retrieve enum members by their description, with
    case-sensitive and case-insensitive variants.
    """

    FORENAMES = "forenames"
    LATEST_RESECT_AND_DISCARD_ACCREDITATION_CREATED_DATE = (
        "latest resect & discard accreditation created date"
    )
    LATEST_RESECT_AND_DISCARD_ACCREDITATION_START_DATE = (
        "latest resect & discard accreditation start date"
    )
    PERSON_ID = "person id"
    PERSON_HAS_CURRENT_ROLE = "person has current role"
    PERSON_HAS_CURRENT_ROLE_IN_ORGANISATION = "person has current role in organisation"
    PERSON_HAS_ENDED_ROLE = "person has ended role"
    PERSON_HAS_ENDED_ROLE_IN_ORGANISATION = "person has ended role in organisation"
    PERSON_HAS_NEVER_HAD_ROLE = "person has never had role"
    PERSON_HAS_NEVER_HAD_ROLE_IN_ORGANISATION = (
        "person has never had role in organisation"
    )
    RESECT_AND_DISCARD_ACCREDITATION_STATUS = "resect & discard accreditation status"
    ROLE_START_DATE = "role start date"
    SURNAME = "surname"

    @classmethod
    def _initialize_lookup_maps(cls) -> None:
        """Initialize the description lookup dictionaries."""
        cls._descriptions = {}
        cls._lowercase_descriptions = {}
        for member in cls:
            cls._descriptions[member.value] = member
            cls._lowercase_descriptions[member.value.lower()] = member

    @classmethod
    def by_description(cls, description: str) -> Optional["PersonSelectionCriteriaKey"]:
        """
        Retrieve an enum member by its exact description.

        Args:
            description (str): The description string to match.

        Returns:
            Optional[PersonSelectionCriteriaKey]: The corresponding enum member,
            or None if no match is found.
        """
        cls._initialize_lookup_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["PersonSelectionCriteriaKey"]:
        """
        Retrieve an enum member by its description, ignoring case.

        Args:
            description (str): The description string to match (case-insensitive).

        Returns:
            Optional[PersonSelectionCriteriaKey]: The corresponding enum member,
            or None if no match is found.
        """
        cls._initialize_lookup_maps()
        return cls._lowercase_descriptions.get(description.lower())
