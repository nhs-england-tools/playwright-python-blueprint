from enum import Enum
from typing import Optional


class DeductionReasonType(Enum):
    """
    Enum representing deduction reason types, mapped to valid value IDs, allowed values, and descriptions.
    Provides utility methods for lookup by description, allowed value, and valid value ID.
    """

    AFL = (307006, "AFL", "AF Enlistment (local)")
    AFN = (307007, "AFN", "AF Enlistment (AF)")
    CGA = (307008, "CGA", "Gone away")
    DEA = (307009, "DEA", "Death")
    Death = (307009, "DEA", "Death")  # Alias for DEA
    DDR = (1, "DDR", "Deducted at Doctor's request")
    DIS = (307010, "DIS", "Practice dissolution")
    DPR = (2, "DPR", "Deducted at Patient's request")
    EMB = (307011, "EMB", "Embarkation")
    Embarkation = (307011, "EMB", "Embarkation")  # Alias for EMB
    FP69 = (17, "FP69", "Deducted as a result of a non-respond to an FP69/")
    LDN = (307012, "LDN", "Logical Deletion")
    MH = (7, "M/H", "Mental Hospital")
    NIT = (307013, "NIT", "Transfer to Northern Ireland")
    OR = (10, "O/R", "Other")
    OPA = (307014, "OPA", "Address out of practice area")
    ORR = (307015, "ORR", "Other Reason")
    PAR = (13, "PAR", "Practice advise subject no longer resident")
    PSR = (14, "PSR", "Practice advise removal via screening system")
    PVR = (15, "PVR", "Practice advise removal via vaccination data")
    R = (26, "R", "Deducted as a result of removal to other HA")
    RA = (8, "R/A", "Registration/A")
    RC = (9, "R/C", "Registration Cancelled")
    RU = (27, "R/U", "Deducted as a result of return undelivered")
    RDI = (307016, "RDI", "Practice Request - immediate")
    RDR = (307017, "RDR", "Practice request")
    RFI = (307018, "RFI", "Residential Institute")
    RPR = (307019, "RPR", "Patient request")
    SD = (6, "S/D", "Service Dependant")
    SCT = (307020, "SCT", "Transferred to Scotland")
    SDL = (307021, "SDL", "Services Dependant (local)")
    SDN = (307022, "SDN", "Services Dependant (SMU)")
    SER = (5, "SER", "Services")
    TRA = (307023, "TRA", "Temporary resident not returned")

    def __init__(
        self, valid_value_id: int, allowed_value: str, description: str
    ) -> None:
        self._valid_value_id = valid_value_id
        self._allowed_value = allowed_value
        self._description = description

    @property
    def valid_value_id(self) -> int:
        """Returns the valid value ID for the deduction reason type."""
        return self._valid_value_id

    @property
    def allowed_value(self) -> str:
        """Returns the allowed value for the deduction reason type."""
        return self._allowed_value

    @property
    def description(self) -> str:
        """Returns the description for the deduction reason type."""
        return self._description

    @classmethod
    def by_description(cls, description: str) -> Optional["DeductionReasonType"]:
        """
        Returns the enum member matching the given description (case-sensitive).
        Args:
            description (str): The description to match.
        Returns:
            Optional[DeductionReasonType]: The matching enum member, or None if not found.
        """
        for member in cls:
            if member.description == description:
                return member
        return None

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["DeductionReasonType"]:
        """
        Returns the enum member matching the given description (case-insensitive).
        Args:
            description (str): The description to match.
        Returns:
            Optional[DeductionReasonType]: The matching enum member, or None if not found.
        """
        desc_lower = description.lower()
        for member in cls:
            if member.description.lower() == desc_lower:
                return member
        return None

    @classmethod
    def by_deduction_code(cls, code: str) -> Optional["DeductionReasonType"]:
        """
        Returns the enum member matching the given allowed value (deduction code).
        Args:
            code (str): The code to match.
        Returns:
            Optional[DeductionReasonType]: The matching enum member, or None if not found.
        """
        code_upper = code.upper()
        for member in cls:
            if member.allowed_value.upper() == code_upper:
                return member
        return None

    @classmethod
    def by_valid_value_id(cls, valid_value_id: int) -> Optional["DeductionReasonType"]:
        """
        Returns the enum member matching the given valid value ID.
        Args:
            valid_value_id (str): The valid_value_id to match.
        Returns:
            Optional[DeductionReasonType]: The matching enum member, or None if not found.
        """
        for member in cls:
            if member.valid_value_id == valid_value_id:
                return member
        return None
