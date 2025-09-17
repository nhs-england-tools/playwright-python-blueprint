from typing import Optional, Union
from dataclasses import dataclass
from datetime import datetime, date
from sys import platform
from classes.address.address_contact_type import AddressContactType
from classes.address.address_type import AddressType
from classes.subject.gender_type import GenderType
from classes.lynch.lynch_sdd_reason_for_change_type import LynchSDDReasonForChangeType
from classes.screening.screening_status_type import ScreeningStatusType
from classes.surveillance.sdd_reason_for_change_type import SDDReasonForChangeType
from classes.screening.ss_reason_for_change_type import SSReasonForChangeType
from classes.surveillance.ssdd_reason_for_change_type import SSDDReasonForChangeType
from classes.user.user import User
from utils.date_time_utils import DateTimeUtils
from utils.oracle.oracle import OracleDB
import pandas as pd
import logging


@dataclass
class Subject:
    """
    Data class representing a subject in the screening system.

    Methods:
        get and set methods for all attributes.
        Utility methods for formatting and describing subject data.
    """

    screening_subject_id: Optional[int] = None
    nhs_number: Optional[str] = None
    surname: Optional[str] = None
    forename: Optional[str] = None
    datestamp: Optional[datetime] = None
    screening_status_id: Optional[int] = None
    screening_status_change_reason_id: Optional[int] = None
    screening_status_change_date: Optional[date] = None
    screening_due_date: Optional[date] = None
    screening_due_date_change_reason_id: Optional[int] = None
    screening_due_date_change_date: Optional[date] = None
    calculated_screening_due_date: Optional[date] = None
    surveillance_screening_due_date: Optional[date] = None
    calculated_surveillance_due_date: Optional[date] = None
    surveillance_due_date_change_reason_id: Optional[int] = None
    surveillance_due_date_change_date: Optional[date] = None
    lynch_due_date: Optional[date] = None
    lynch_due_date_change_reason_id: Optional[int] = None
    lynch_due_date_change_date: Optional[date] = None
    calculated_lynch_due_date: Optional[date] = None
    date_of_birth: Optional[date] = None
    age: int = 0

    other_names: Optional[str] = None
    previous_surname: Optional[str] = None
    title: Optional[str] = None
    date_of_death: Optional[date] = None
    gender: Optional["GenderType"] = None
    address_type: Optional["AddressType"] = None
    address_contact_type: Optional["AddressContactType"] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    address_line4: Optional[str] = None
    address_line5: Optional[str] = None
    postcode: Optional[str] = None
    address_effective_from: Optional[date] = None
    address_effective_to: Optional[date] = None
    registration_code: Optional[str] = None
    gp_practice_id: Optional[int] = None
    gp_practice_code: Optional[str] = None
    nhais_deduction_reason: Optional[str] = None
    nhais_deduction_date: Optional[date] = None
    datasource: Optional[str] = None
    removed_to_datasource: Optional[str] = None
    audit_reason: Optional[str] = None
    contact_id: Optional[int] = None

    def get_screening_subject_id(self) -> Optional[int]:
        """
        Returns the screening subject ID.

        Returns:
            Optional[int]: The screening subject ID.
        """
        return self.screening_subject_id

    def set_screening_subject_id(self, screening_subject_id: int) -> None:
        """
        Sets the screening subject ID.

        Args:
            screening_subject_id (int): The screening subject ID to set.
        """
        self.screening_subject_id = screening_subject_id

    def get_nhs_number(self) -> Optional[str]:
        """
        Returns the NHS number.

        Returns:
            Optional[str]: The NHS number.
        """
        return self.nhs_number

    def get_nhs_number_spaced(self) -> Optional[str]:
        """
        Returns the NHS number with spaces for readability if it is 10 digits.

        Returns:
            Optional[str]: The formatted NHS number, or the original if not 10 digits.
        """
        if self.nhs_number and len(self.nhs_number) == 10:
            return f"{self.nhs_number[:3]} {self.nhs_number[3:6]} {self.nhs_number[6:]}"
        return self.nhs_number

    def set_nhs_number(self, nhs_number: str):
        """
        Sets the NHS number.

        Args:
            nhs_number (str): The NHS number to set.
        """
        self.nhs_number = nhs_number

    def get_surname(self) -> Optional[str]:
        """
        Returns the surname.

        Returns:
            Optional[str]: The surname.
        """
        return self.surname

    def set_surname(self, surname: str) -> None:
        """
        Sets the surname.

        Args:
            surname (str): The surname to set.
        """
        self.surname = surname

    def get_forename(self) -> Optional[str]:
        """
        Returns the forename.

        Returns:
            Optional[str]: The forename.
        """
        return self.forename

    def set_forename(self, forname: str) -> None:
        """
        Sets the forename.

        Args:
            forname (str): The forename to set.
        """
        self.forename = forname

    def get_datestamp(self) -> Optional[datetime]:
        """
        Returns the datestamp.

        Returns:
            Optional[datetime]: The datestamp.
        """
        return self.datestamp

    def set_datestamp(self, datestamp: datetime) -> None:
        """
        Sets the datestamp.

        Args:
            datestamp (datetime): The datestamp to set.
        """
        self.datestamp = datestamp

    def get_full_name(self) -> Optional[str]:
        """
        Returns the full name, including title, forename, and surname.

        Returns:
            Optional[str]: The full name.
        """
        title_part = f"{self.title}" if self.title else ""
        return f"{title_part} {self.forename} {self.surname}"

    def get_forename_surname(self) -> Optional[str]:
        """
        Returns the forename and surname.

        Returns:
            Optional[str]: The forename and surname.
        """
        return f"{self.forename} {self.surname}"

    def get_name_and_nhs_number(self) -> Optional[str]:
        """
        Returns the forename, surname, and NHS number.

        Returns:
            Optional[str]: The formatted name and NHS number.
        """
        return f"{self.forename} {self.surname} (NHS# {self.nhs_number})"

    def get_screening_status_id(self) -> Optional[int]:
        """
        Returns the screening status ID.

        Returns:
            Optional[int]: The screening status ID.
        """
        return self.screening_status_id

    def set_screening_status_id(self, screening_status_id: int) -> None:
        """
        Sets the screening status ID.

        Args:
            screening_status_id (int): The screening status ID to set.
        """
        self.screening_status_id = screening_status_id

    def get_screening_due_date(self) -> Optional[date]:
        """
        Returns the screening due date.

        Returns:
            Optional[date]: The screening due date.
        """
        return self.screening_due_date

    def set_screening_due_date(self, screening_due_date: date) -> None:
        """
        Sets the screening due date.

        Args:
            screening_due_date (date): The screening due date to set.
        """
        self.screening_due_date = screening_due_date

    def get_calculated_screening_due_date(self) -> Optional[date]:
        """
        Returns the calculated screening due date.

        Returns:
            Optional[date]: The calculated screening due date.
        """
        return self.calculated_screening_due_date

    def set_calculated_screening_due_date(
        self, calculated_screening_due_date: date
    ) -> None:
        """
        Sets the calculated screening due date.

        Args:
            calculated_screening_due_date (date): The calculated screening due date to set.
        """
        self.calculated_screening_due_date = calculated_screening_due_date

    def get_lynch_due_date(self) -> Optional[date]:
        """
        Returns the Lynch due date.

        Returns:
            Optional[date]: The Lynch due date.
        """
        return self.lynch_due_date

    def set_lynch_due_date(self, lynch_due_date: date) -> None:
        """
        Sets the Lynch due date.

        Args:
            lynch_due_date (date): The Lynch due date to set.
        """
        self.lynch_due_date = lynch_due_date

    def get_lynch_due_date_change_reason_id(self) -> Optional[int]:
        """
        Returns the Lynch due date change reason ID.

        Returns:
            Optional[int]: The Lynch due date change reason ID.
        """
        return self.lynch_due_date_change_reason_id

    def set_lynch_due_date_change_reason_id(
        self, lynch_due_date_change_reason_id: int
    ) -> None:
        """
        Sets the Lynch due date change reason ID.

        Args:
            lynch_due_date_change_reason_id (int): The Lynch due date change reason ID to set.
        """
        self.lynch_due_date_change_reason_id = lynch_due_date_change_reason_id

    def get_lynch_due_date_change_date(self) -> Optional[date]:
        """
        Returns the Lynch due date change date.

        Returns:
            Optional[date]: The Lynch due date change date.
        """
        return self.lynch_due_date_change_date

    def set_lynch_due_date_change_date(self, lynch_due_date_change_date: date) -> None:
        """
        Sets the Lynch due date change date.

        Args:
            lynch_due_date_change_date (date): The Lynch due date change date to set.
        """
        self.lynch_due_date_change_date = lynch_due_date_change_date

    def get_calculated_lynch_due_date(self) -> Optional[date]:
        """
        Returns the calculated Lynch due date.

        Returns:
            Optional[date]: The calculated Lynch due date.
        """
        return self.calculated_lynch_due_date

    def set_calculated_lynch_due_date(self, calculated_lynch_due_date: date) -> None:
        """
        Sets the calculated Lynch due date.

        Args:
            calculated_lynch_due_date (date): The calculated Lynch due date to set.
        """
        self.calculated_lynch_due_date = calculated_lynch_due_date

    def get_surveillance_screening_due_date(self) -> Optional[date]:
        """
        Returns the surveillance screening due date.

        Returns:
            Optional[date]: The surveillance screening due date.
        """
        return self.surveillance_screening_due_date

    def set_surveillance_screening_due_date(
        self, surveillance_screening_due_date: date
    ):
        """
        Sets the surveillance screening due date.

        Args:
            surveillance_screening_due_date (date): The surveillance screening due date to set.
        """
        self.surveillance_screening_due_date = surveillance_screening_due_date

    def get_calculated_surveillance_due_date(self) -> Optional[date]:
        """
        Returns the calculated surveillance due date.

        Returns:
            Optional[date]: The calculated surveillance due date.
        """
        return self.calculated_surveillance_due_date

    def set_calculated_surveillance_due_date(
        self, calculated_surveillance_due_date: date
    ) -> None:
        """
        Sets the calculated surveillance due date.

        Args:
            calculated_surveillance_due_date (date): The calculated surveillance due date to set.
        """
        self.calculated_surveillance_due_date = calculated_surveillance_due_date

    def get_date_of_birth(self) -> Optional[date]:
        """
        Returns the date of birth.

        Returns:
            Optional[date]: The date of birth.
        """
        return self.date_of_birth

    def get_date_of_deth(self) -> Optional[date]:
        """
        Returns the date of death.

        Returns:
            Optional[date]: The date of death.
        """
        return self.date_of_death

    def set_date_of_birth(self, dob: Optional[date]) -> None:
        """
        Sets the date of birth and updates the age accordingly.

        Args:
            dob (Optional[date]): The date of birth to set.
        """
        self.date_of_birth = dob
        if dob is None:
            self.age = 0
        else:
            today = date.today()
            self.age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )

    def get_age(self) -> Optional[int]:
        """
        Returns the age.

        Returns:
            Optional[int]: The age.
        """
        return self.age

    def get_date_of_birth_string(self) -> Optional[str]:
        """
        Returns the date of birth as a string in numeric format.

        Returns:
            Optional[str]: The formatted date of birth.
        """
        return self.get_date_as_string(self.date_of_birth, False)

    def get_date_of_birth_string_text_month(self) -> Optional[str]:
        """
        Returns the date of birth as a string with the month as text.

        Returns:
            Optional[str]: The formatted date of birth.
        """
        return self.get_date_as_string(self.date_of_birth, True)

    def get_date_of_birth_with_age(self) -> Optional[str]:
        """
        Returns the date of birth string with age.

        Returns:
            Optional[str]: The formatted date of birth with age.
        """
        return f"{self.get_date_of_birth_string()} (age: {self.age})"

    def get_date_of_birth_text_month_with_age(self) -> Optional[str]:
        """
        Returns the date of birth string with month as text and age.

        Returns:
            Optional[str]: The formatted date of birth with age.
        """
        return f"{self.get_date_of_birth_string_text_month()} (age: {self.age})"

    def get_date_of_death_string(self) -> Optional[str]:
        """
        Returns the date of death as a string.

        Returns:
            Optional[str]: The formatted date of death.
        """
        return self.get_date_as_string(self.date_of_death, False)

    def get_screening_status_change_date_string(self) -> Optional[str]:
        """
        Returns the screening status change date as a string.

        Returns:
            Optional[str]: The formatted screening status change date.
        """
        return self.get_date_as_string(self.screening_status_change_date, False)

    def get_screening_due_date_string(self) -> Optional[str]:
        """
        Returns the screening due date as a string.

        Returns:
            Optional[str]: The formatted screening due date.
        """
        return self.get_date_as_string(self.screening_due_date, False)

    def get_screening_due_date_change_date_string(self) -> Optional[str]:
        """
        Returns the screening due date change date as a string.

        Returns:
            Optional[str]: The formatted screening due date change date.
        """
        return self.get_date_as_string(self.screening_due_date_change_date, False)

    def get_lynch_due_date_change_date_string(self) -> Optional[str]:
        """
        Returns the Lynch due date change date as a string.

        Returns:
            Optional[str]: The formatted Lynch due date change date.
        """
        return self.get_date_as_string(self.lynch_due_date_change_date, False)

    def get_calculated_screening_due_date_string(self) -> Optional[str]:
        """
        Returns the calculated screening due date as a string.

        Returns:
            Optional[str]: The formatted calculated screening due date.
        """
        return self.get_date_as_string(self.calculated_screening_due_date, False)

    def get_calculated_lynch_due_date_string(self) -> Optional[str]:
        """
        Returns the calculated Lynch due date as a string.

        Returns:
            Optional[str]: The formatted calculated Lynch due date.
        """
        return self.get_date_as_string(self.calculated_lynch_due_date, False)

    def get_surveillance_screening_due_date_string(self) -> Optional[str]:
        """
        Returns the surveillance screening due date as a string.

        Returns:
            Optional[str]: The formatted surveillance screening due date.
        """
        return self.get_date_as_string(self.surveillance_screening_due_date, False)

    def get_calculated_surveillance_due_date_string(self) -> Optional[str]:
        """
        Returns the calculated surveillance due date as a string.

        Returns:
            Optional[str]: The formatted calculated surveillance due date.
        """
        return self.get_date_as_string(self.calculated_surveillance_due_date, False)

    def get_surveillance_due_date_change_date_string(self) -> Optional[str]:
        """
        Returns the surveillance due date change date as a string.

        Returns:
            Optional[str]: The formatted surveillance due date change date.
        """
        return self.get_date_as_string(self.surveillance_due_date_change_date, False)

    def get_lynch_due_date_string(self) -> Optional[str]:
        """
        Returns the Lynch due date as a string.

        Returns:
            Optional[str]: The formatted Lynch due date.
        """
        return self.get_date_as_string(self.lynch_due_date, False)

    def get_screening_status_id_desc(self) -> Optional[str]:
        """
        Returns the screening status ID and its description.

        Returns:
            Optional[str]: The formatted screening status ID and description.
        """
        if self.screening_status_id is not None:
            status_type = ScreeningStatusType.by_valid_value_id(
                self.screening_status_id
            )
            if status_type is not None:
                description = status_type.description
                return f"{self.screening_status_id} {description}"
        return None

    def get_screening_status_change_reason_id_desc(self) -> Optional[str]:
        """
        Returns the screening status change reason ID and its description.

        Returns:
            Optional[str]: The formatted screening status change reason ID and description.
        """
        if self.screening_status_change_reason_id is not None:
            reason_type = SSReasonForChangeType.by_valid_value_id(
                self.screening_status_change_reason_id
            )
            if reason_type is not None:
                description = reason_type.description
                return f"{self.screening_status_change_reason_id} {description}"
        return None

    def get_screening_due_date_change_reason_id_desc(self) -> Optional[str]:
        """
        Returns the screening due date change reason ID and its description.

        Returns:
            Optional[str]: The formatted screening due date change reason ID and description.
        """
        if self.screening_due_date_change_reason_id is not None:
            reason_type = SDDReasonForChangeType.by_valid_value_id(
                self.screening_due_date_change_reason_id
            )
            if reason_type is not None:
                description = reason_type.description
                return f"{self.screening_due_date_change_reason_id} {description}"
        return None

    def get_lynch_due_date_change_reason_id_desc(self) -> Optional[str]:
        """
        Returns the Lynch due date change reason ID and its description.

        Returns:
            Optional[str]: The formatted Lynch due date change reason ID and description.
        """
        if self.lynch_due_date_change_reason_id is not None:
            reason_type = LynchSDDReasonForChangeType.by_valid_value_id(
                self.lynch_due_date_change_reason_id
            )
            if reason_type is not None:
                description = reason_type.description
                return f"{self.lynch_due_date_change_reason_id} {description}"
        return None

    def get_surveillance_due_date_change_reason_id_desc(self) -> Optional[str]:
        """
        Returns the surveillance due date change reason ID and its description.

        Returns:
            Optional[str]: The formatted surveillance due date change reason ID and description.
        """
        if self.surveillance_due_date_change_reason_id is not None:
            reason_type = SSDDReasonForChangeType.by_valid_value_id(
                self.surveillance_due_date_change_reason_id
            )
            if reason_type is not None:
                description = reason_type.description
                return f"{self.surveillance_due_date_change_reason_id} {description}"
        return None

    def get_date_as_string(
        self, date_to_convert: Optional[Union[date, datetime]], month_as_text: bool
    ) -> Optional[str]:
        """
        Returns a date as a string, optionally with the month as text.

        Args:
            date_to_convert (Optional[Union[date, datetime]]): The date to convert.
            month_as_text (bool): Whether to use the month as text.

        Returns:
            Optional[str]: The formatted date string.
        """
        if date_to_convert is None:
            return None

        if isinstance(date_to_convert, date) and not isinstance(
            date_to_convert, datetime
        ):
            date_to_convert = datetime.combine(date_to_convert, datetime.min.time())

        if platform == "win32":  # Windows:
            format_to_use = "%#d %b %Y" if month_as_text else "%d/%m/%Y"
        else:
            format_to_use = "%-d %b %Y" if month_as_text else "%d/%m/%Y"
        return date_to_convert.strftime(format_to_use)

    def get_other_names(self) -> Optional[str]:
        """
        Returns other names.

        Returns:
            Optional[str]: The other names.
        """
        return self.other_names

    def set_other_names(self, other_names: str) -> None:
        """
        Sets other names.

        Args:
            other_names (str): The other names to set.
        """
        self.other_names = other_names

    def get_previous_surname(self) -> Optional[str]:
        """
        Returns the previous surname.

        Returns:
            Optional[str]: The previous surname.
        """
        return self.previous_surname

    def set_previous_surname(self, previous_surname: str) -> None:
        """
        Sets the previous surname.

        Args:
            previous_surname (str): The previous surname to set.
        """
        self.previous_surname = previous_surname

    def get_title(self) -> Optional[str]:
        """
        Returns the title.

        Returns:
            Optional[str]: The title.
        """
        return self.title

    def set_title(self, title: str) -> None:
        """
        Sets the title.

        Args:
            title (str): The title to set.
        """
        self.title = title

    def get_gender(self) -> Optional["GenderType"]:
        """
        Returns the gender.

        Returns:
            Optional[GenderType]: The gender.
        """
        return self.gender

    def set_gender(self, gender: "GenderType") -> None:
        """
        Sets the gender.

        Args:
            gender (GenderType): The gender to set.
        """
        self.gender = gender

    def get_address_line_1(self) -> Optional[str]:
        """
        Returns address line 1.

        Returns:
            Optional[str]: Address line 1.
        """
        return self.address_line_1

    def set_address_line_1(self, address_line_1: str) -> None:
        """
        Sets address line 1.

        Args:
            address_line_1 (str): Address line 1 to set.
        """
        self.address_line_1 = address_line_1

    def get_address_line_2(self) -> Optional[str]:
        """
        Returns address line 2.

        Returns:
            Optional[str]: Address line 2.
        """
        return self.address_line_2

    def set_address_line_2(self, address_line_2: str) -> None:
        """
        Sets address line 2.

        Args:
            address_line_2 (str): Address line 2 to set.
        """
        self.address_line_2 = address_line_2

    def get_address_line_3(self) -> Optional[str]:
        """
        Returns address line 3.

        Returns:
            Optional[str]: Address line 3.
        """
        return self.address_line_3

    def set_address_line_3(self, address_line_3: str) -> None:
        """
        Sets address line 3.

        Args:
            address_line_3 (str): Address line 3 to set.
        """
        self.address_line_3 = address_line_3

    def get_address_line_4(self) -> Optional[str]:
        """
        Returns address line 4.

        Returns:
            Optional[str]: Address line 4.
        """
        return self.address_line_4

    def set_address_line_4(self, address_line_4: str) -> None:
        """
        Sets address line 4.

        Args:
            address_line_4 (str): Address line 4 to set.
        """
        self.address_line_4 = address_line_4

    def get_address_line_5(self) -> Optional[str]:
        """
        Returns address line 5.

        Returns:
            Optional[str]: Address line 5.
        """
        return self.address_line_5

    def set_address_line_5(self, address_line_5: str) -> None:
        """
        Sets address line 5.

        Args:
            address_line_5 (str): Address line 5 to set.
        """
        self.address_line_5 = address_line_5

    def get_address_type(self) -> Optional["AddressType"]:
        """
        Returns the address type.

        Returns:
            Optional[AddressType]: The address type.
        """
        return self.address_type

    def set_address_type(self, address_type: "AddressType") -> None:
        """
        Sets the address type.

        Args:
            address_type (AddressType): The address type to set.
        """
        self.address_type = address_type

    def get_address_contact_type(self) -> Optional["AddressContactType"]:
        """
        Returns the address contact type.

        Returns:
            Optional[AddressContactType]: The address contact type.
        """
        return self.address_contact_type

    def set_address_contact_type(
        self, address_contact_type: "AddressContactType"
    ) -> None:
        """
        Sets the address contact type.

        Args:
            address_contact_type (AddressContactType): The address contact type to set.
        """
        self.address_contact_type = address_contact_type

    def get_postcode(self) -> Optional[str]:
        """
        Returns the postcode.

        Returns:
            Optional[str]: The postcode.
        """
        return self.postcode

    def set_postcode(self, postcode: str) -> None:
        """
        Sets the postcode.

        Args:
            postcode (str): The postcode to set.
        """
        self.postcode = postcode

    def get_address_effective_from(self) -> Optional[date]:
        """
        Returns the address effective from date.

        Returns:
            Optional[date]: The address effective from date.
        """
        return self.address_effective_from

    def set_address_effective_from(self, address_effective_from: date) -> None:
        """
        Sets the address effective from date.

        Args:
            address_effective_from (date): The address effective from date to set.
        """
        self.address_effective_from = address_effective_from

    def get_address_effective_to(self) -> Optional[date]:
        """
        Returns the address effective to date.

        Returns:
            Optional[date]: The address effective to date.
        """
        return self.address_effective_to

    def set_address_effective_to(self, address_effective_to: date) -> None:
        """
        Sets the address effective to date.

        Args:
            address_effective_to (date): The address effective to date to set.
        """
        self.address_effective_to = address_effective_to

    def get_registration_code(self) -> Optional[str]:
        """
        Returns the registration code.

        Returns:
            Optional[str]: The registration code.
        """
        return self.registration_code

    def set_registration_code(self, registration_code: str) -> None:
        """
        Sets the registration code.

        Args:
            registration_code (str): The registration code to set.
        """
        self.registration_code = registration_code

    def get_gp_practice_id(self) -> Optional[int]:
        """
        Returns the GP practice ID.

        Returns:
            Optional[int]: The GP practice ID.
        """
        return self.gp_practice_id

    def set_gp_practice_id(self, gp_practice_id: int) -> None:
        """
        Sets the GP practice ID.

        Args:
            gp_practice_id (int): The GP practice ID to set.
        """
        self.gp_practice_id = gp_practice_id

    def get_gp_practice_code(self) -> Optional[str]:
        """
        Returns the GP practice code.

        Returns:
            Optional[str]: The GP practice code.
        """
        return self.gp_practice_code

    def set_gp_practice_code(self, gp_practice_code: str) -> None:
        """
        Sets the GP practice code.

        Args:
            gp_practice_code (str): The GP practice code to set.
        """
        self.gp_practice_code = gp_practice_code

    def get_nhais_deduction_reason(self) -> Optional[str]:
        """
        Returns the NHAIS deduction reason.

        Returns:
            Optional[str]: The NHAIS deduction reason.
        """
        return self.nhais_deduction_reason

    def set_nhais_deduction_reason(self, nhais_deduction_reason: str) -> None:
        """
        Sets the NHAIS deduction reason.

        Args:
            nhais_deduction_reason (str): The NHAIS deduction reason to set.
        """
        self.nhais_deduction_reason = nhais_deduction_reason

    def get_nhais_deduction_date(self) -> Optional[date]:
        """
        Returns the NHAIS deduction date.

        Returns:
            Optional[date]: The NHAIS deduction date.
        """
        return self.nhais_deduction_date

    def set_nhais_deduction_date(self, nhais_deduction_date: date) -> None:
        """
        Sets the NHAIS deduction date.

        Args:
            nhais_deduction_date (date): The NHAIS deduction date to set.
        """
        self.nhais_deduction_date = nhais_deduction_date

    def get_datasource(self) -> Optional[str]:
        """
        Returns the data source.

        Returns:
            Optional[str]: The data source.
        """
        return self.datasource

    def set_datasource(self, datasource: str) -> None:
        """
        Sets the data source.

        Args:
            datasource (str): The data source to set.
        """
        self.datasource = datasource

    def get_removed_to_datasource(self) -> Optional[str]:
        """
        Returns the removed to data source.

        Returns:
            Optional[str]: The removed to data source.
        """
        return self.removed_to_datasource

    def set_removed_to_datasource(self, removed_to_datasource: str) -> None:
        """
        Sets the removed to data source.

        Args:
            removed_to_datasource (str): The removed to data source to set.
        """
        self.removed_to_datasource = removed_to_datasource

    def get_audit_reason(self) -> Optional[str]:
        """
        Returns the audit reason.

        Returns:
            Optional[str]: The audit reason.
        """
        return self.audit_reason

    def set_audit_reason(self, audit_reason: str) -> None:
        """
        Sets the audit reason.

        Args:
            audit_reason (str): The audit reason to set.
        """
        self.audit_reason = audit_reason

    def get_contact_id(self) -> Optional[int]:
        """
        Returns the contact ID.

        Returns:
            Optional[int]: The contact ID.
        """
        return self.contact_id

    def set_contact_id(self, contact_id: int) -> None:
        """
        Sets the contact ID.

        Args:
            contact_id (int): The contact ID to set.
        """
        self.contact_id = contact_id

    def get_screening_status_change_reason_id(self) -> Optional[int]:
        """
        Returns the screening status change reason ID.

        Returns:
            Optional[int]: The screening status change reason ID.
        """
        return self.screening_status_change_reason_id

    def set_screening_status_change_reason_id(
        self, screening_status_change_reason_id: int
    ) -> None:
        """
        Sets the screening status change reason ID.

        Args:
            screening_status_change_reason_id (int): The screening status change reason ID to set.
        """
        self.screening_status_change_reason_id = screening_status_change_reason_id

    def get_screening_status_change_date(self) -> Optional[date]:
        """
        Returns the screening status change date.

        Returns:
            Optional[date]: The screening status change date.
        """
        return self.screening_status_change_date

    def set_screening_status_change_date(
        self, screening_status_change_date: date
    ) -> None:
        """
        Sets the screening status change date.

        Args:
            screening_status_change_date (date): The screening status change date to set.
        """
        self.screening_status_change_date = screening_status_change_date

    def get_screening_due_date_change_reason_id(self) -> Optional[int]:
        """
        Returns the screening due date change reason ID.

        Returns:
            Optional[int]: The screening due date change reason ID.
        """
        return self.screening_due_date_change_reason_id

    def set_screening_due_date_change_reason_id(
        self, screening_due_date_change_reason_id: int
    ) -> None:
        """
        Sets the screening due date change reason ID.

        Args:
            screening_due_date_change_reason_id (int): The screening due date change reason ID to set.
        """
        self.screening_due_date_change_reason_id = screening_due_date_change_reason_id

    def get_screening_due_date_change_date(self) -> Optional[date]:
        """
        Returns the screening due date change date.

        Returns:
            Optional[date]: The screening due date change date.
        """
        return self.screening_due_date_change_date

    def set_screening_due_date_change_date(
        self, screening_due_date_change_date: date
    ) -> None:
        """
        Sets the screening due date change date.

        Args:
            screening_due_date_change_date (date): The screening due date change date to set.
        """
        self.screening_due_date_change_date = screening_due_date_change_date

    def get_surveillance_due_date_change_reason_id(self) -> Optional[int]:
        """
        Returns the surveillance due date change reason ID.

        Returns:
            Optional[int]: The surveillance due date change reason ID.
        """
        return self.surveillance_due_date_change_reason_id

    def set_surveillance_due_date_change_reason_id(
        self, surveillance_due_date_change_reason_id: int
    ) -> None:
        """
        Sets the surveillance due date change reason ID.

        Args:
            surveillance_due_date_change_reason_id (int): The surveillance due date change reason ID to set.
        """
        self.surveillance_due_date_change_reason_id = (
            surveillance_due_date_change_reason_id
        )

    def get_surveillance_due_date_change_date(self) -> Optional[date]:
        """
        Returns the surveillance due date change date.

        Returns:
            Optional[date]: The surveillance due date change date.
        """
        return self.surveillance_due_date_change_date

    def set_surveillance_due_date_change_date(
        self, surveillance_due_date_change_date: date
    ) -> None:
        """
        Sets the surveillance due date change date.

        Args:
            surveillance_due_date_change_date (date): The surveillance due date change date to set.
        """
        self.surveillance_due_date_change_date = surveillance_due_date_change_date

    def value_or_null(self, value):
        """
        Returns "null" if the value is None, otherwise returns the value.

        Args:
            value: The value to check.

        Returns:
            Any: "null" if value is None, else the value.
        """
        return "null" if value is None else value

    def __str__(self):
        """
        Returns a string representation of the Subject object.

        Returns:
            str: The string representation of the subject.
        """
        return (
            f"Subject ["
            f"screeningSubjectId={self.screening_subject_id}, "
            f"nhsNumber={self.nhs_number}, "
            f"forename={self.forename}, "
            f"surname={self.surname}, "
            f"dateOfBirth={self.value_or_null(self.get_date_of_birth_with_age())}, "
            f"dateOfDeath={self.value_or_null(self.get_date_of_death_string())}, "
            f"screeningStatusId={self.value_or_null(self.get_screening_status_id_desc())}, "
            f"screeningStatusChangeReasonId={self.value_or_null(self.get_screening_status_change_reason_id_desc())}, "
            f"screeningStatusChangeDate={self.value_or_null(self.get_screening_status_change_date_string())}, "
            f"screeningDueDate={self.value_or_null(self.get_screening_due_date_string())}, "
            f"screeningDueDateChangeReasonId={self.value_or_null(self.get_screening_due_date_change_reason_id_desc())}, "
            f"screeningDueDateChangeDate={self.value_or_null(self.get_screening_due_date_change_date_string())}, "
            f"calculatedScreeningDueDate={self.value_or_null(self.get_calculated_screening_due_date_string())}, "
            f"surveillanceScreeningDueDate={self.value_or_null(self.get_surveillance_screening_due_date_string())}, "
            f"calculatedSurveillanceDueDate={self.value_or_null(self.get_calculated_surveillance_due_date_string())}, "
            f"surveillanceDueDateChangeReasonId={self.value_or_null(self.get_surveillance_due_date_change_reason_id_desc())}, "
            f"surveillanceDueDateChangeDate={self.value_or_null(self.get_surveillance_due_date_change_date_string())}, "
            f"lynchDueDate={self.value_or_null(self.get_lynch_due_date_string())}, "
            f"lynchDueDateChangeReasonId={self.value_or_null(self.get_lynch_due_date_change_reason_id_desc())}, "
            f"lynchDueDateChangeDate={self.value_or_null(self.get_lynch_due_date_change_date_string())}, "
            f"calculatedLynchDueDate={self.value_or_null(self.get_calculated_lynch_due_date_string())}, "
            f"gpPracticeCode={self.value_or_null(self.gp_practice_code)}, "
            f"nhaisDeductionReason={self.value_or_null(self.nhais_deduction_reason)}, "
            f"datestamp={self.datestamp}"
            f"]"
        )

    @staticmethod
    def from_dataframe_row(row: pd.Series) -> "Subject":
        """
        Populates a Subject object from a pandas DataFrame row.
        Handles type conversions for dates and datetimes.
        Only fields present in the SQL query are populated.
        """

        field_map = {
            "screening_subject_id": row.get("screening_subject_id"),
            "nhs_number": row.get("subject_nhs_number"),
            "surname": row.get("person_family_name"),
            "forename": row.get("person_given_name"),
            "datestamp": DateTimeUtils.parse_datetime(row.get("datestamp")),
            "screening_status_id": row.get("screening_status_id"),
            "screening_status_change_reason_id": row.get("ss_reason_for_change_id"),
            "screening_status_change_date": DateTimeUtils.parse_date(
                row.get("screening_status_change_date")
            ),
            "screening_due_date": DateTimeUtils.parse_date(
                row.get("screening_due_date")
            ),
            "screening_due_date_change_reason_id": row.get("sdd_reason_for_change_id"),
            "screening_due_date_change_date": DateTimeUtils.parse_date(
                row.get("sdd_change_date")
            ),
            "calculated_screening_due_date": DateTimeUtils.parse_date(
                row.get("calculated_sdd")
            ),
            "surveillance_screening_due_date": DateTimeUtils.parse_date(
                row.get("surveillance_screen_due_date")
            ),
            "calculated_surveillance_due_date": DateTimeUtils.parse_date(
                row.get("calculated_ssdd")
            ),
            "surveillance_due_date_change_reason_id": row.get(
                "surveillance_sdd_rsn_change_id"
            ),
            "surveillance_due_date_change_date": DateTimeUtils.parse_date(
                row.get("surveillance_sdd_change_date")
            ),
            "lynch_due_date": DateTimeUtils.parse_date(
                row.get("lynch_screening_due_date")
            ),
            "lynch_due_date_change_reason_id": row.get(
                "lynch_sdd_reason_for_change_id"
            ),
            "lynch_due_date_change_date": DateTimeUtils.parse_date(
                row.get("lynch_sdd_change_date")
            ),
            "calculated_lynch_due_date": DateTimeUtils.parse_date(
                row.get("lynch_calculated_sdd")
            ),
            "date_of_birth": DateTimeUtils.parse_date(row.get("date_of_birth")),
            "date_of_death": DateTimeUtils.parse_date(row.get("date_of_death")),
        }

        return Subject(**field_map)

    def populate_subject_object_from_nhs_no(self, nhs_no: str) -> "Subject":
        """
        Populates a Subject object from the NHS number.
        Args:
            nhs_no (str): The NHS number to populate the subject from.
        Returns:
            Subject: A populated Subject object from the database
        """
        from utils.oracle.subject_selection_query_builder import (
            SubjectSelectionQueryBuilder,
        )

        nhs_no_criteria = {"nhs number": nhs_no}
        subject = Subject()
        user = User()
        builder = SubjectSelectionQueryBuilder()

        query, bind_vars = builder.build_subject_selection_query(
            criteria=nhs_no_criteria,
            user=user,
            subject=subject,
            subjects_to_retrieve=1,
        )

        logging.debug(
            "[SUBJECT ASSERTIONS] Executing base query to populate subject object"
        )

        subject_df = OracleDB().execute_query(query, bind_vars)
        return self.from_dataframe_row(subject_df.iloc[0])
