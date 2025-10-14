from enum import Enum
from typing import Optional


class RoleType(Enum):
    """
    Enum representing role types, mapped to valid value IDs and descriptions.
    Provides utility methods for lookup by description (case-sensitive and insensitive) and by valid value ID.
    """

    ACCREDITED_SCREENING_COLONOSCOPIST = (5069, "Accredited Screening Colonoscopist")
    ACCREDITED_SCREENING_FLEXIBLE_SIGMOIDOSCOPIST = (
        203009,
        "Accredited Screening Flexible Sigmoidoscopist",
    )
    ASPIRANT_ENDOSCOPIST = (305587, "Aspirant Endoscopist")
    ASSISTANT_LABORATORY_LEAD_STATE_REGISTERED = (
        309006,
        "Assistant Laboratory Lead - state registered",
    )
    ASSISTANT_SCREENING_PRACTITIONER = (202254, "Assistant Screening Practitioner")
    BCSS_AUTOMATED_HUB_PROCESS = (309025, "BCSS Automated Hub Process")
    BCSS_AUTOMATED_PROCESS = (5044, "BCSS Automated Process")
    BCSS_BUREAU_STAFF = (5042, "BCSS Bureau Staff")
    BCSS_DATABASE_ADMINISTRATOR = (5043, "BCSS Database Administrator")
    BCSS_SUPPORT_HUB = (202245, "BCSS Support - Hub")
    BCSS_SUPPORT_ICB = (202248, "BCSS Support - ICB")
    BCSS_SUPPORT_SC = (202246, "BCSS Support - SC")
    CANCER_WAITING_TIMES_ADMINISTRATOR = (5061, "Cancer Waiting Times Administrator")
    CONSULTANT_COLONOSCOPIST = (5045, "Consultant Colonoscopist")
    CONSULTANT_GASTROENTEROLOGIST = (5054, "Consultant Gastroenterologist")
    CONSULTANT_ONCOLOGIST = (5047, "Consultant Oncologist")
    CONSULTANT_PATHOLOGIST = (5049, "Consultant Pathologist")
    CONSULTANT_RADIOLOGIST = (5050, "Consultant Radiologist")
    CONSULTANT_SURGEON = (5051, "Consultant Surgeon")
    FS_SCREENING_COORDINATOR = (5073, "FS Screening Coordinator")
    HUB_DASHBOARD_USER = (309010, "Hub Dashboard User")
    HUB_DATA_ANALYST = (5063, "Hub Data Analyst")
    HUB_DIRECTOR_STATE_REGISTERED = (309009, "Hub Director - state registered")
    HUB_MANAGER = (309007, "Hub Manager")
    HUB_MANAGER_STATE_REGISTERED = (309008, "Hub Manager - state registered")
    HUB_PILOT = (306407, "Hub Pilot")
    INFORMATION_OFFICER = (5070, "Information Officer")
    MDT_COORDINATOR = (5052, "MDT co-ordinator")
    NATIONAL_BCS_ADMINISTRATOR = (5030, "National BCS Administrator")
    NATIONAL_DASHBOARD_USER = (202482, "National Dashboard User")
    NATIONAL_DATA_ANALYST = (5064, "National Data Analyst")
    NATIONAL_PILOT = (306406, "National Pilot")
    NATIONAL_QA_USER = (202193, "National QA User")
    NON_SCREENING_NURSE = (5048, "Non Screening Nurse")
    NURSE_CONSULTANT = (5053, "Nurse Consultant")
    PI_BCSS_BUREAU = (5072, "PI BCSS Bureau")
    QA_ENDOSCOPY_LEAD = (5058, "QA Endoscopy Lead")
    QA_ENDOSCOPY_NATIONAL_LEAD = (5057, "QA Endoscopy National Lead")
    QA_ENDOSCOPY_SCREENING_CENTRE_LEAD = (5059, "QA Endoscopy Screening Centre Lead")
    QA_NATIONAL_NURSE_ADVISOR = (5055, "QA National Nurse Advisor")
    QA_REGIONAL_LEAD_NURSE = (5056, "QA Regional Lead Nurse")
    QA_TEAM_USER = (202192, "QA Team User")
    REGIONAL_DASHBOARD_USER = (5075, "Regional Dashboard User")
    REGIONAL_QA_USER = (5062, "Regional QA User")
    REPORTING_RADIOGRAPHER = (5068, "Reporting Radiographer")
    REPORTING_RADIOLOGIST = (5067, "Reporting Radiologist")
    SCREENING_ASSISTANT = (309003, "Screening Assistant")
    SCREENING_CENTRE_CLERK = (5040, "Screening Centre Clerk")
    SCREENING_CENTRE_DASHBOARD_USER = (5065, "Screening Centre Dashboard User")
    SCREENING_CENTRE_MANAGER = (5039, "Screening Centre Manager")
    SCREENING_CENTRE_PILOT = (306405, "Screening Centre Pilot")
    SCREENING_PRACTITIONER = (202253, "Screening Practitioner")
    SENIOR_SCREENING_ASSISTANT = (309004, "Senior Screening Assistant")
    SPECIALIST_PALLIATIVE_CARE_CONSULTANT = (
        202373,
        "Specialist Palliative Care Consultant",
    )
    SPECIALIST_SCREENING_PRACTITIONER = (5041, "Specialist Screening Practitioner")
    TEAM_LEADER = (309005, "Team Leader")
    TESTING_RADIOGRAPHER = (5066, "Testing Radiographer")

    def __init__(self, valid_value_id: int, description: str) -> None:
        self._valid_value_id = valid_value_id
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the role type."""
        return self._valid_value_id

    @property
    def description(self) -> str:
        """Returns the description for the role type."""
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["RoleType"]:
        """
        Returns the enum member matching the given description (case-sensitive).
        """
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_description_case_insensitive(cls, description: str) -> Optional["RoleType"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["RoleType"]:
        """
        Returns the enum member matching the given valid value ID.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
