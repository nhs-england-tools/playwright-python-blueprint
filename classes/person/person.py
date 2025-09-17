import logging
from typing import Optional
from classes.subject.gender_type import GenderType


class Person:
    """
    Represents a person with name, title, gender, and other attributes.
    """

    def __init__(self) -> None:
        self.surname: str = ""
        self.forename: str = ""
        self.title: str = ""
        self.other_forenames: str = ""
        self.previous_surname: str = ""
        self.gender: Optional[GenderType] = GenderType.NOT_KNOWN

    def get_full_name(self) -> str:
        """
        Returns the full name of the person, including title, forename, and surname.
        """
        return f"{self.title} {self.forename} {self.surname}"

    def __str__(self) -> str:
        """
        Returns a string representation of the person, including gender.
        """
        return f"{self.title} {self.forename} {self.surname} (gender={self.gender})"

    def get_surname(self) -> str:
        """
        Returns the surname of the person.
        """
        return self.surname

    def set_surname(self, surname: str) -> None:
        """
        Sets the surname of the person.
        """
        logging.debug("set surname")
        self.surname = surname

    def get_forename(self) -> str:
        """
        Returns the forename of the person.
        """
        return self.forename

    def set_forename(self, forename: str) -> None:
        """
        Sets the forename of the person.
        """
        logging.debug("set forename")
        self.forename = forename

    def get_title(self) -> str:
        """
        Returns the title of the person.
        """
        return self.title

    def set_title(self, title: str) -> None:
        """
        Sets the title of the person.
        """
        logging.debug("set title")
        self.title = title

    def get_other_forenames(self) -> str:
        """
        Returns other forenames of the person.
        """
        return self.other_forenames

    def set_other_forenames(self, other_forenames: str) -> None:
        """
        Sets other forenames of the person.
        """
        logging.debug("set other_forenames")
        self.other_forenames = other_forenames

    def get_previous_surname(self) -> str:
        """
        Returns the previous surname of the person.
        """
        return self.previous_surname

    def set_previous_surname(self, previous_surname: str) -> None:
        """
        Sets the previous surname of the person.
        """
        logging.debug("set previous_surname")
        self.previous_surname = previous_surname

    def get_gender(self) -> Optional[GenderType]:
        """
        Returns the gender of the person.
        """
        return self.gender

    def set_gender(self, gender: GenderType) -> None:
        """
        Sets the gender of the person.
        """
        logging.debug("set gender")
        self.gender = gender
