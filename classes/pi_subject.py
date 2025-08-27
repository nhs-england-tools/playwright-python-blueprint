from dataclasses import dataclass, field
from typing import Optional
from datetime import date


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
