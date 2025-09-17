from enum import Enum
from typing import Optional, Dict

redirect_to_confirm_string = "Redirect to Confirm Diagnostic Test Result and Outcome"


class EventCodeType(Enum):
    """
    Enum representing event codes with IDs, codes, and descriptions.
    """

    E1 = (11001, "E1", "Select for Screening")
    E2 = (11078, "E2", "Change Diagnostic Test Data")
    E5 = (160100, "E5", "Enter Diagnostic Test Outcome")
    E6 = (160220, "E6", "Enter Diagnostic Test Outcome")
    E7 = (305488, "E7", "Record Diagnosis Date")
    E8 = (305496, "E8", "Amend Diagnosis Date")
    E9 = (305497, "E9", "Confirm no Diagnosis Date")
    E17 = (11003, "E17", "Suitability Decision")
    E22 = (11004, "E22", "Test Kit Result")
    E26 = (160231, "E26", "Discard Diagnostic Test")
    E27 = (11075, "E27", "Redirect to DELETE the Latest Diagnostic Test Result")
    E28 = (160213, "E28", redirect_to_confirm_string)
    E29 = (160226, "E29", redirect_to_confirm_string)
    E30 = (20432, "E30", "Redirect to Re-record the Outcome of Symptomatic Referral")
    E31 = (11080, "E31", "Redirect to Re-record Patient Contact")
    E32 = (202076, "E32", redirect_to_confirm_string)
    E33 = (306400, "E33", "Reset kit")
    E43 = (11005, "E43", "Refer for Clinician Review")
    E44 = (11006, "E44", "Pending")
    E46 = (11007, "E46", "Provide Screening Centre Assistance")
    E49 = (11008, "E49", "Provide Programme Hub Assistance")
    E52 = (11009, "E52", "Pending Decision to Proceed with Diagnostic Test")
    E55 = (11010, "E55", "Log a kit")
    E56 = (11011, "E56", "Send Pre-Invitation Letter")
    E57 = (11012, "E57", "Send Opt-In Confirmation and Pre-Invitation Letter")
    E58 = (11013, "E58", "Send Initial Kit")
    E59 = (200522, "E59", "Initiate Opt-in/Self-referral")
    E60 = (11014, "E60", "Send Retest Kit")
    E61 = (
        11015,
        "E61",
        "Reopen after Unexpected Abnormal or Weak Positive Kit Received",
    )
    E62 = (11016, "E62", "Reopen following Non-Response")
    E63 = (11017, "E63", "Reopen episode for correction")
    E64 = (11018, "E64", "Reopen following Incorrect Test Reading")
    E65 = (11019, "E65", "Send a kit")
    E66 = (11020, "E66", "Reopen for Self-Referral")
    E67 = (160215, "E67", "Reopen to Confirm Diagnostic Test Result and Outcome")
    E68 = (20442, "E68", "Reopen to Reschedule Diagnostic Test")
    E70 = (11079, "E70", "Reopen after Returned/Undelivered Mail")
    E71 = (11081, "E71", "Automatic reopen after Returned/Undelivered Mail")
    E72 = (200523, "E72", "Reopen due to subject or patient decision")
    E77 = (11021, "E77", "Send New Kit")
    E78 = (11022, "E78", "Log Kit")
    E80 = (20338, "E80", "Colonoscopy Assessment Appointment Rescheduled")
    E81 = (20339, "E81", "Reschedule Post-Investigation appointment")
    E82 = (20340, "E82", "Reschedule Surveillance appointment")
    E83 = (20341, "E83", "Colonoscopy assessment appointment new letter requested")
    E84 = (20342, "E84", "Post-Investigation appointment new letter request")
    E85 = (20343, "E85", "Surveillance appointment new letter request")
    E95 = (11023, "E95", "Send Reminder Letter")
    E96 = (160195, "E96", "Confirm Colonoscopy")
    E97 = (160196, "E97", "Attend Diagnostic Test")
    E99 = (160224, "E99", "System Episode Progression")
    E100 = (306111, "E100", "Reopen for Screening Incident = (Retest Kit)")
    E101 = (306112, "E101", "Reopen for Screening Incident = (Replacement Kit)")
    E102 = (306113, "E102", "Redirect for Screening Incident = (Retest Kit)")
    E103 = (306114, "E103", "Redirect for Screening Incident = (Replacement Kit)")
    E113 = (11024, "E113", "New Kit Required following Spoilt Assistance")
    E116 = (11025, "E116", "Non-response following Spoilt Assistance")
    E119 = (11026, "E119", "Send Normal Result Letter to Subject")
    E120 = (11027, "E120", "Send Normal Result Communication to GP")
    E123 = (11028, "E123", "Send Abnormal Result Communication to GP")
    E124 = (11029, "E124", "Request Assessment Appointment and create letter")
    E125 = (
        11030,
        "E125",
        "Request Assessment Appointment following a DNA and create letter",
    )
    E126 = (11031, "E126", "Book Assessment Appointment")
    E127 = (11032, "E127", "Book Assessment Appointment following a DNA")
    E128 = (11033, "E128", "Cancel Assessment Appointment")
    E129 = (11034, "E129", "Cancel 1st Colonoscopy Assessment Appointment")
    E130 = (11035, "E130", "Cancel Assessment Appointment = (follows a DNA)")
    E131 = (11036, "E131", "Cancel 2nd Colonoscopy Assessment Appointment")
    E132 = (11065, "E132", "Cancel Appointment Prior to Letter Preparation")
    E133 = (
        11066,
        "E133",
        "Cancel Appointment Prior to Letter Preparation = (follows a DNA)",
    )
    E139 = (205216, "E139", "Colonoscopy Assessment Appointment Required")
    E140 = (11037, "E140", "Screening Centre does not Attend Appointment")
    E141 = (
        11038,
        "E141",
        "Screening Centre Does Not Attend 1st Colonoscopy Assessment Appointment",
    )
    E142 = (
        11039,
        "E142",
        "Screening Centre does not Attend Appointment following a DNA",
    )
    E143 = (
        11040,
        "E143",
        "Screening Centre Does Not Attend 2nd Colonoscopy Assessment Appointment",
    )
    E144 = (11041, "E144", "Attend Colonoscopy Assessment Appointment")
    E145 = (11042, "E145", "Patient does not Attend Assessment Appointment")
    E146 = (11043, "E146", "Send Missed Assessment Appointment letter")
    E147 = (11044, "E147", "Invite for Colonoscopy")
    E148 = (11045, "E148", "Invite for Diagnostic Test")
    E149 = (11046, "E149", "Request New Kit")
    E150 = (11047, "E150", "Continue from Pending")
    E151 = (11048, "E151", "Redirect to Provide Screening Centre Assistance")
    E152 = (11049, "E152", "Refuse Colonoscopy Assessment Appointment")
    E153 = (11050, "E153", "Send Discharge Letter to Patient")
    E154 = (11051, "E154", "Screening Centre Discharge Patient")
    E156 = (
        11052,
        "E156",
        "Patient does not Attend Assessment Appointment following a DNA",
    )
    E159 = (11053, "E159", "Receive Decision to Proceed with Another Test")
    E161 = (11054, "E161", "No Decision Received to Proceed with Diagnostic Tests")
    E162 = (11055, "E162", "DNA Diagnostic Test")
    E163 = (203154, "E163", "Subject DNA Diagnostic Test")
    E164 = (203155, "E164", "Screening Centre DNA Diagnostic Test")
    E166 = (11002, "E166", "Postpone Surveillance Episode")
    E167 = (11056, "E167", "Initiate Close")
    E168 = (11064, "E168", "Close Episode")
    E171 = (11058, "E171", "Redirect to Provide Hub Level Assistance")
    E172 = (11059, "E172", "Redirect to Receive Unexpected Test Kit")
    E173 = (11060, "E173", "Redirect following Incorrect Test Kit Reading")
    E174 = (11061, "E174", "Redirect to Create Assessment Appointment")
    E175 = (11062, "E175", "Redirect to Establish Suitability for Diagnostic Tests")
    E177 = (11067, "E177", "Queue Letter")
    E178 = (11068, "E178", "Cancel Communication")
    E179 = (11071, "E179", "Print Supplementary Batch Letter")
    E180 = (11072, "E180", "Reprint Letter")
    E181 = (11073, "E181", "Print Redundant Letter")
    E182 = (160234, "E182", "Create letter for 30 Day Questionnaire")
    E183 = (160117, "E183", "Redirect to Establish Attendance at Appointment")
    E184 = (160118, "E184", "Reopen to Amend Assessment Appointment")
    E185 = (20240, "E185", "Print 30 Day Questionnaire")
    E186 = (160199, "E186", "Redirect to Re-Confirm Diagnostic Test")
    E187 = (160235, "E187", "Select episode for a 30 Day Questionnaire")
    E188 = (200214, "E188", "Send Additional GP Communication")
    E200 = (200665, "E200", "Update Screening Subject Status")
    E201 = (200666, "E201", "Update bowel scope Screening Due Date")
    E202 = (200667, "E202", "Update Screening Due Date")
    E203 = (208091, "E203", "Update Surveillance Screening Due Date")
    E204 = (305453, "E204", "Reopen to book an assessment appointment")
    E205 = (305556, "E205", "Complete surveillance review")
    E206 = (305714, "E206", "Update Lynch Surveillance Due Date")
    E227 = (
        160217,
        "E227",
        "Redirect to put the Latest Diagnostic Test Result back to CONFIRMED ONLY",
    )
    E348 = (202091, "E348", "Redirect to Re-establish Suitability for Colonoscopy")
    E349 = (
        160233,
        "E349",
        "Redirect to re-establish suitability for diagnostic test re:patient contact",
    )
    E350 = (160114, "E350", "Record Contact with Patient")
    E351 = (160214, "E351", "Post-investigation Appointment has Already Taken Place")
    E352 = (160223, "E352", "Record other post-investigation contact")
    E353 = (34, "E353", "Subject Requested Cease - Record Patient Contact not Required")
    E354 = (202074, "E354", "Col. Assessment Appointment Required Decision")
    E355 = (160104, "E355", "Post-Investigation Appointment Required Decision")
    E356 = (160228, "E356", "Decision whether or not to Refer MDT")
    E357 = (202075, "E357", "Complete Colonoscopy Assessment Dataset")
    E358 = (202101, "E358", "Create Col. Assessment Dataset")
    E360 = (160102, "E360", "Handover into Symptomatic Care")
    E361 = (160116, "E361", "Print Handover into Symptomatic Care Letter to GP")
    E370 = (20307, "E370", "Create and Send Diagnostic Test Result letter to GP")
    E372 = (20309, "E372", "Reopen to Re-record Outcome from Symptomatic Referral")
    E375 = (
        160108,
        "E375",
        "Post-investigation clinic patient diagnostic result letter printed = (Spur event)",
    )
    E378 = (204321, "E378", "Print Patient Result Letter")
    E379 = (204320, "E379", "Print GP Result Letter")
    E380 = (160101, "E380", "Send Diagnostic Test Result to Patient")
    E381 = (20133, "E381", "Send Diagnostic Test Result to GP")
    E382 = (305791, "E382", "Send Symptomatic Procedure Result to Patient")
    E395 = (
        11074,
        "E395",
        "Redirect for Another Diagnostic Test on Direction of Clinician",
    )
    E396 = (160192, "E396", "Patient Refuses Another Diagnostic Test")
    E397 = (
        160191,
        "E397",
        "Patient Can Not be Contacted to Arrange Another Diagnostic Test",
    )
    E400 = (160105, "E400", "Book Post-Investigation Appointment")
    E401 = (160107, "E401", "Send Post-Investigation Appointment Letter")
    E410 = (
        160106,
        "E410",
        "Post-Investigation Appointment Cancelled before Invitation Letters Prepared",
    )
    E415 = (160115, "E415", "Patient Attends Post-Investigation Appointment")
    E417 = (160109, "E417", "SC Cancelled Post-Investigation Appointment")
    E420 = (160110, "E420", "Patient Cancelled Post-Investigation Appointment")
    E425 = (
        160111,
        "E425",
        "Screening Practitioner Does Not Attend Post-Investigation Appointment",
    )
    E426 = (160216, "E426", "Post-investigation Appointment Attended")
    E441 = (160112, "E441", "Patient Does Not Attend Post-Investigation Appointment")
    E500 = (20134, "E500", "Surveillance Selection")
    E501 = (20135, "E501", "Record No Contact from Patient")
    E505 = (20136, "E505", "Record MDT Appointment")
    E510 = (20137, "E510", "Print Surveillance HC Form")
    E515 = (20138, "E515", "Record Outcome from Symptomatic Referral")
    E517 = (20139, "E517", "Enter Alternative Screening Interval")
    E520 = (20140, "E520", "Enter Patient Assessment Dataset")
    E530 = (83, "E530", "Non-neoplastic and Other Non-bowel Cancer Result")
    E531 = (85, "E531", "Low-risk Result from Symptomatic Procedure")
    E532 = (87, "E532", "Intermediate-risk Result from Symptomatic Procedure")
    E533 = (89, "E533", "High-risk Result from Symptomatic Procedure")
    E534 = (91, "E534", "Cancer Outcome from Symptomatic Procedure")
    E535 = (305621, "E535", "LNPCP Result from Symptomatic Procedure")
    E536 = (305620, "E536", "High-risk findings Result from Symptomatic Procedure")
    E600 = (20141, "E600", "Book Surveillance Appointment")
    E601 = (20143, "E601", "Send Surveillance Appointment Letter")
    E610 = (
        20142,
        "E610",
        "Surveillance Appointment Cancelled before Invitation Letters Prepared",
    )
    E617 = (20144, "E617", "SC Cancelled Surveillance Appointment")
    E620 = (20145, "E620", "Patient Cancelled Surveillance Appointment")
    E622 = (20187, "E622", "Send Surveillance Cancellation Letter")
    E625 = (
        20146,
        "E625",
        "Screening Practitioner Does Not Attend Surveillance Appointment",
    )
    E641 = (20147, "E641", "Patient Does Not Attend Surveillance Appointment")
    E650 = (
        20186,
        "E650",
        "Patient & Screening Practitioner Attend Surveillance Appointment",
    )
    E701 = (200658, "E701", "Select for bowel scope Screening")
    E702 = (200659, "E702", "Send bowel scope Screening Pre-Invitation")
    E703 = (200660, "E703", "Send bowel scope Screening Invitation and appointment")
    E704 = (200661, "E704", "Initiate self-referral for bowel scope Screening")
    E705 = (200677, "E705", "Select for bowel scope Screening Reminder")
    E705E = (
        208045,
        "E705E",
        "Record bowel scope response prior to re-booking a BS appointment",
    )
    E705A = (208036, "E705A", "Record bowel scope response received by telephone")
    E705B = (
        208037,
        "E705B",
        "Record bowel scope response prior to BS Suitability Assessment",
    )
    E705C = (
        208038,
        "E705C",
        "Record bowel scope response prior to booking a BS appointment",
    )
    E705D = (208039, "E705D", "Record bowel scope response received by paper form")
    E706 = (200678, "E706", "Send bowel scope Screening Reminder")
    E707 = (200679, "E707", "Select for bowel scope Screening Reminder Non-Response")
    E708 = (200680, "E708", "Send bowel scope Screening Reminder Non-Response")
    E709 = (206060, "E709", "Request cancellation of bowel scope Appointment")
    E710 = (206061, "E710", "Book bowel scope Appointment")
    E711 = (206062, "E711", "Cancel bowel scope Appointment")
    E712 = (206063, "E712", "Print bowel scope Appointment Invitation")
    E713 = (206064, "E713", "Book another bowel scope Appointment")
    E714 = (206065, "E714", "Initiate bowel scope Pre-invitation processing")
    E715 = (206001, "E715", "Link initial bowel scope appointment to episode")
    E716 = (206066, "E716", "Book bowel scope Appointment in Confirmed List")
    E717 = (208031, "E717", "Patient not available for offered appointment")
    E718 = (205030, "E718", "Confirm bowel scope Appointment")
    E719 = (208044, "E719", "Print bowel scope Appointment Confirmation Letter")
    E720 = (204026, "E720", "Request bowel scope Bowel Prep")
    E721 = (203057, "E721", "Print Subject letter on manual close")
    E722 = (203058, "E722", "Print GP letter on manual close")
    E723 = (206067, "E723", "Bowel scope Appointment not available")
    E724 = (206005, "E724", "Select for bowel scope Screening Reminder")
    E725 = (
        206068,
        "E725",
        "Identify insufficient bowel scope Screening availability at Screening Centre",
    )
    E726 = (208057, "E726", "Assessed as NOT suitable for bowel scope")
    E727 = (208058, "E727", "Send NOT suitable for bowel scope = (subject) Letter")
    E728 = (208059, "E728", "Send NOT suitable for bowel scope = (GP) Letter")
    E729 = (
        208060,
        "E729",
        "Unable to contact subject to complete bowel scope Suitability Assessment",
    )
    E730 = (
        208061,
        "E730",
        "Send unable to contact subject to complete bowel scope Screening Suitability Assessment = (subject) letter",
    )
    E731 = (
        208062,
        "E731",
        "Send unable to contact subject to complete bowel scope Suitability Assessment = (GP) letter",
    )
    E732 = (206070, "E732", "Book bowel scope Appointment = (no letter)")
    E733 = (
        205070,
        "E733",
        "Request Colonoscopy Assessment Appointment and create letter",
    )
    E734 = (
        205071,
        "E734",
        "Reschedule Colonoscopy Assessment Appointment before printing letter",
    )
    E735 = (
        205072,
        "E735",
        "SC Cancels Colonoscopy Assessment Appointment before letter Preparation",
    )
    E736 = (205073, "E736", "Book Colonoscopy Assessment Appointment")
    E737 = (205035, "E737", "Subject non responded from bowel scope Screening")
    E738 = (205074, "E738", "Cancel Colonoscopy Assessment Appointment")
    E739 = (205075, "E739", "Send Patient Cancels to Consider letter")
    E740 = (205076, "E740", "Attend Colonoscopy Assessment Appointment")
    E741 = (205077, "E741", "SC does not Attend Colonoscopy Assessment Appointment")
    E742 = (
        205078,
        "E742",
        "Patient does not Attend Colonoscopy Assessment Appointment",
    )
    E743 = (205079, "E743", "Patient Discharged, Cancelled to Consider")
    E744 = (
        205080,
        "E744",
        "Patient Discharged, DNA Colonoscopy Assessment Appointment",
    )
    E745 = (205081, "E745", "Transfer to Post-investigation, no patient letter")
    E746 = (205082, "E746", "Send Missed Colonoscopy Assessment Appointment letter")
    E747 = (205036, "E747", "Send non response letter to subject")
    E748 = (
        205083,
        "E748",
        "Transfer to Post-investigation pathway as Colonoscopy Assessment not required",
    )
    E749 = (205084, "E749", "Transfer to Colonoscopy Assessment pathway")
    E750 = (205033, "E750", "Issue bowel scope Bowel Prep")
    E751 = (205034, "E751", "Request another bowel scope Bowel Prep")
    E752 = (206104, "E752", "Cancel bowel scope Appointment before printing letter")
    E753 = (205085, "E753", "Transfer to Post-investigation, patient letter required")
    E754 = (204107, "E754", "Link FIT Device to Episode")
    E801 = (307072, "E801", "Select for Lynch Surveillance")
    E802 = (307073, "E802", "Send Lynch pre-invitation letter")
    E803 = (307074, "E803", "Request assessment appointment")
    E804 = (307082, "E804", "Establish suitability for Lynch Surveillance")
    E805 = (307083, "E805", "Continue Lynch Surveillance Episode")
    E806 = (307087, "E806", "Close Lynch Surveillance Episode = (Recent Colonoscopy)")
    E807 = (307092, "E807", "Print Subject Letter = (Recent Colonoscopy)")
    E808 = (307088, "E808", "Close Lynch Surveillance Episode = (Incorrect Diagnosis)")
    E809 = (307093, "E809", "Print Subject Letter = (Incorrect Lynch Diagnosis)")
    E810 = (307094, "E810", "Print GP Letter = (Incorrect Lynch Diagnosis)")
    E811 = (307091, "E811", "Reopen to review suitability for Lynch Surveillance")
    E812 = (307105, "E812", "Close Lynch Surveillance Episode = (Clinical Reason)")
    E813 = (307106, "E813", "Print Subject Letter = (Clinical Reason)")
    E814 = (307107, "E814", "Print GP Letter = (Clinical Reason)")
    E850 = (305759, "E850", "Request NHS App message")
    E851 = (305762, "E851", "NHS App message read")
    E852 = (305763, "E852", "Unread NHS App message")
    E999 = (160227, "E999", "Phase 3 Release System Episode Progression")

    def __init__(self, id: int, code: str, description: str):
        self._id: int = id
        self._code: str = code
        self._description: str = description

    @property
    def id(self) -> int:
        """Returns the event code ID."""
        return self._id

    @property
    def code(self) -> str:
        """Returns the event code string."""
        return self._code

    @property
    def description(self) -> str:
        """Returns the event code description."""
        return self._description

    @classmethod
    def _build_maps(cls) -> None:
        """
        Initializes internal lookup maps for EventCodeType enum members.

        It ensures these maps are built only once per class, using `hasattr` to prevent
        redundant reinitialization.
        """
        if not hasattr(cls, "_codes"):
            cls._codes: Dict[str, EventCodeType] = {}
            cls._descriptions: Dict[str, EventCodeType] = {}
            cls._lowercase_descriptions: Dict[str, EventCodeType] = {}
            cls._ids: Dict[int, EventCodeType] = {}
            for item in cls:
                cls._codes[item.code] = item
                cls._descriptions[item.description] = item
                cls._lowercase_descriptions[item.description.lower()] = item
                cls._ids[item.id] = item

    @classmethod
    def by_code(cls, code: str) -> Optional["EventCodeType"]:
        """
        Returns the EventCodeType matching the given code.
        """
        cls._build_maps()
        return cls._codes.get(code)

    @classmethod
    def by_description(cls, description: str) -> Optional["EventCodeType"]:
        """
        Returns the EventCodeType matching the given description.
        """
        cls._build_maps()
        return cls._descriptions.get(description)

    @classmethod
    def by_description_case_insensitive(
        cls, description: str
    ) -> Optional["EventCodeType"]:
        """
        Returns the EventCodeType matching the given description (case-insensitive).
        """
        cls._build_maps()
        return cls._lowercase_descriptions.get(description.lower())

    @classmethod
    def by_id(cls, id: int) -> Optional["EventCodeType"]:
        """
        Returns the EventCodeType matching the given ID.
        """
        cls._build_maps()
        return cls._ids.get(id)

    def get_id(self) -> int:
        """Returns the event code ID."""
        return self._id

    def get_code(self) -> str:
        """Returns the event code string."""
        return self._code

    def get_description(self) -> str:
        """Returns the event code description."""
        return self._description
