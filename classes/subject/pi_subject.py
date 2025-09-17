from dataclasses import dataclass, field
from typing import Optional
from datetime import date
from classes.subject.subject import Subject


@dataclass
class PISubject:
    """
    Represents a PI Subject with all relevant demographic and administrative fields.
    """

    screening_subject_id: Optional[int] = None
    nhs_number: Optional[str] = None
    family_name: Optional[str] = None
    first_given_names: Optional[str] = None
    other_given_names: Optional[str] = None
    previous_family_name: Optional[str] = None
    name_prefix: Optional[str] = None
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    gender_code: Optional[int] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    address_line_3: Optional[str] = None
    address_line_4: Optional[str] = None
    address_line_5: Optional[str] = None
    postcode: Optional[str] = None
    gnc_code: Optional[str] = None
    gp_practice_code: Optional[str] = None
    nhais_deduction_reason: Optional[str] = None
    nhais_deduction_date: Optional[date] = None
    exeter_system: Optional[str] = None
    removed_to: Optional[str] = None
    pi_reference: Optional[str] = None
    superseded_by_nhs_number: Optional[str] = None
    replaced_nhs_number: Optional[str] = None

    def to_string(self) -> str:
        """
        Returns a string representation of the PISubject object, showing all field names and values.
        Each field is on a new line with extra spacing for readability.
        Useful for logging and debugging.
        """
        fields = [
            f"screening_subject_id    =    {self.screening_subject_id}",
            f"nhs_number              =    {self.nhs_number}",
            f"family_name             =    {self.family_name}",
            f"first_given_names       =    {self.first_given_names}",
            f"other_given_names       =    {self.other_given_names}",
            f"previous_family_name    =    {self.previous_family_name}",
            f"name_prefix             =    {self.name_prefix}",
            f"birth_date              =    {self.birth_date}",
            f"death_date              =    {self.death_date}",
            f"gender_code             =    {self.gender_code}",
            f"address_line1           =    {self.address_line_1}",
            f"address_line2           =    {self.address_line_2}",
            f"address_line3           =    {self.address_line_3}",
            f"address_line4           =    {self.address_line_4}",
            f"address_line5           =    {self.address_line_5}",
            f"post_code               =    {self.postcode}",
            f"registration_code       =    {self.gnc_code}",
            f"gp_practice_code        =    {self.gp_practice_code}",
            f"nhais_deduction_reason  =    {self.nhais_deduction_reason}",
            f"nhais_deduction_date    =    {self.nhais_deduction_date}",
            f"exeter_system           =    {self.exeter_system}",
            f"removed_to              =    {self.removed_to}",
            f"pi_reference            =    {self.pi_reference}",
            f"superseded_by_nhs_number=    {self.superseded_by_nhs_number}",
            f"replaced_by_nhs_number  =    {self.replaced_nhs_number}",
        ]
        return "PISubject:\n" + "\n".join(fields)

    @staticmethod
    def from_subject(subject: "Subject") -> "PISubject":
        """
        Creates a PISubject object from a Subject object.

        Args:
            subject (Subject): The Subject object to convert.

        Returns:
            PISubject: The populated PISubject object.

        """
        gender = subject.get_gender()
        if gender is not None:
            gender_code = gender.redefined_value
        else:
            gender_code = 0  # If None, set to "Not known gender"
        return PISubject(
            screening_subject_id=subject.screening_subject_id,
            nhs_number=subject.nhs_number,
            family_name=subject.surname,
            first_given_names=subject.forename,
            other_given_names=subject.other_names,
            previous_family_name=subject.previous_surname,
            name_prefix=subject.title,
            birth_date=subject.date_of_birth,
            death_date=subject.date_of_death,
            gender_code=gender_code,
            address_line_1=subject.address_line1,
            address_line_2=subject.address_line2,
            address_line_3=subject.address_line3,
            address_line_4=subject.address_line4,
            address_line_5=subject.address_line5,
            postcode=subject.postcode,
            gnc_code=subject.registration_code,
            gp_practice_code=subject.gp_practice_code,
            nhais_deduction_reason=subject.nhais_deduction_reason,
            nhais_deduction_date=subject.nhais_deduction_date,
            exeter_system=subject.datasource,
            removed_to=subject.removed_to_datasource,
            pi_reference=None,
            superseded_by_nhs_number=None,
            replaced_nhs_number=None,
        )
