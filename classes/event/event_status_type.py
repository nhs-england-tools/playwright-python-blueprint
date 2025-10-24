from enum import Enum
from typing import Optional


class EventStatusType(Enum):
    """
    Enum representing various event status types for screening and diagnostic events.

    Each member contains:
        - id (int): The unique identifier for the event status.
        - code (str): The event status code.
        - description (str): A human-readable description of the event status.

    Example members:
        A100: Suitable for Radiological Test
        A101: Pending decision to proceed with Endoscopic Test
        ...
        U98: Weak Positive, Waiting for Programme Hub Assistance

    Methods:
        id: Returns the unique identifier for the event status.
        code: Returns the event status code.
        description: Returns the human-readable description of the event status.
        get_by_id(id_: int) -> Optional[EventStatusType]: Returns the enum member matching the given id.
        get_by_code(code: str) -> Optional[EventStatusType]: Returns the enum member matching the given code.
        get_by_description(description: str) -> Optional[EventStatusType]: Returns the enum member matching the given description.
    """

    A100 = (11101, "A100", "Suitable for Radiological Test")
    A101 = (11102, "A101", "Pending decision to proceed with Endoscopic Test")
    A103 = (11103, "A103", "No Decision Received to Proceed with Diagnostic Tests")
    A156 = (160185, "A156", "Intermediate-risk Adenoma")
    A157 = (305616, "A157", "LNPCP")
    A158 = (305617, "A158", "High-risk findings")
    A165 = (11105, "A165", "Waiting Decision to Proceed with Diagnostic Test")
    A166 = (
        11106,
        "A166",
        "GP Discharge Sent (No show for Colonoscopy Assessment Appointment)",
    )
    A167 = (11107, "A167", "GP Abnormal FOBT Result Sent")
    A168 = (
        11108,
        "A168",
        "GP Discharge Sent (No Agreement to Proceed with Diagnostic Tests)",
    )
    A172 = (160152, "A172", "DNA Diagnostic Test")
    A183 = (11111, "A183", "1st Colonoscopy Assessment Appointment Requested")
    A184 = (11112, "A184", "2nd Colonoscopy Assessment Appointment Requested")
    A185 = (
        11113,
        "A185",
        "2nd Colonoscopy Assessment Appointment Non-attendance (Patient)",
    )
    A196 = (11114, "A196", "Follow Up Questionnaire Sent (Abnormal Finding)")
    A197 = (11115, "A197", "Removed from phase 2A")
    A198 = (11116, "A198", "Follow Up Questionnaire Sent (High-risk Adenoma)")
    A199 = (11117, "A199", "Follow Up Questionnaire Sent (Intermediate-risk Adenoma)")
    A200 = (11118, "A200", "Follow Up Questionnaire Sent (Low-risk Adenoma)")
    A227 = (160193, "A227", "Confirmed Diagnostic Test")
    A227A259 = (
        160225,
        "A227/A259",
        "Redirect back to A227 or A259 (depending on the previous Diagnostic Test)",
    )
    A25 = (11119, "A25", "1st Colonoscopy Assessment Appointment Booked, letter sent")
    A259 = (160194, "A259", "Attended Diagnostic Test")
    A26 = (11120, "A26", "2nd Colonoscopy Assessment Appointment Booked, letter sent")
    A27 = (11121, "A27", "Invited for Colonoscopy")
    A27A59 = (
        160190,
        "A27/A59",
        "Redirect back to A27 or A59 (depending on the previous Diagnostic Test)",
    )
    A300 = (160154, "A300", "Failed Test - Refer Another")
    A305 = (160203, "A305", "Consent Refused, Refer Another")
    A306 = (160169, "A306", "Cancel Diagnostic Test")
    A307 = (160222, "A307", "Consent Refused (prior to investigation)")
    A309 = (204298, "A309", "Normal, Return to FOBT, GP Communication Created")
    A310 = (160205, "A310", "Withdrawn Consent, Refer Another")
    A315 = (160206, "A315", "Diagnostic Test Outcome Entered")
    A316 = (160218, "A316", "Post-investigation Appointment Attended")
    A317 = (160219, "A317", "Post-investigation Contact Made")
    A318 = (
        160221,
        "A318",
        "Post-investigation Appointment NOT Required - Result Letter Created",
    )
    A319 = (
        305787,
        "A319",
        "Refer follow-up test after return from symptomatic referral letter (Patient & GP)",
    )
    A320 = (160160, "A320", "Refer Another Test")
    A321 = (203141, "A321", "Manual Patient Result Letter Created")
    A322 = (203142, "A322", "GP Copy of Manual Patient Result Letter on Queue")
    A323 = (160182, "A323", "Post-investigation Appointment NOT Required")
    A324 = (
        204304,
        "A324",
        "Post-investigation Appt Attended, Normal Result, GP Communication Created",
    )
    A325 = (
        204295,
        "A325",
        "Attended Not Screened, Return to FOBT, Patient Result Letter Created",
    )
    A326 = (
        204296,
        "A326",
        "Attended Not Screened, Return to FOBT, GP Communication Created",
    )
    A327 = (204297, "A327", "Normal, Return to FOBT, Patient Result Letter Created")
    A328 = (204313, "A328", "Handover into Symptomatic Care (Bowel scope)")
    A329 = (
        204299,
        "A329",
        "Post-investigation Appt Attended, Abnormal Patient Result Letter Created",
    )
    A330 = (
        204301,
        "A330",
        "Post-investigation Appt Attended, Attended Not Screened Patient Result Letter Created",
    )
    A331 = (
        204303,
        "A331",
        "Post-investigation Appt Attended, Normal Patient Result Letter Created",
    )
    A335 = (
        204300,
        "A335",
        "Post-investigation Appt Attended, Abnormal Result, GP Communication Created",
    )
    A336 = (
        204302,
        "A336",
        "Post-investigation Appt Attended, Attended Not Screened Result, GP Communication Created",
    )
    A338 = (204305, "A338", "Abnormal, Return to FOBT, Patient Result Letter Created")
    A339 = (204306, "A339", "Abnormal, Return to FOBT, GP Communication Created")
    A340 = (160155, "A340", "Normal (No Abnormalities Found)")
    A341 = (160156, "A341", "Low-risk Adenoma")
    A342 = (160157, "A342", "Intermediate-risk Adenoma")
    A343 = (160158, "A343", "High-risk Adenoma")
    A344 = (160159, "A344", "Abnormal")
    A345 = (160153, "A345", "Cancer Result, Refer MDT")
    A346 = (160163, "A346", "Handover into Symptomatic Care")
    A347 = (20074, "A347", "Refer to Symptomatic")
    A348 = (20075, "A348", "MDT Referral Required")
    A350 = (
        160166,
        "A350",
        "Letter of Non-agreement to Continue with Investigation sent to GP",
    )
    A351 = (160168, "A351", "GP Discharge Letter Printed - No Patient Contact")
    A352 = (160162, "A352", "Non-attendance of Diagnostic Test - DNA Letter Printed")
    A353 = (20229, "A353", "MDT Referral Not Required")
    A354 = (20123, "A354", "Contact Outcome = SSP Appointment Required")
    A355 = (20124, "A355", "Contact Outcome = Further Contact Required")
    A356 = (
        20428,
        "A356",
        "Handover into Symptomatic Care, Patient Unfit, GP Letter Printed",
    )
    A357 = (20429, "A357", "Patient Unfit, Handover into Symptomatic Care")
    A358 = (202000, "A358", "Return to FOBT After Symptomatic Referral")
    A360 = (160171, "A360", "Post-investigation Appointment Required")
    A361 = (160172, "A361", "Other Post-investigation Contact Required")
    A362 = (20078, "A362", "Refer to surgery - Post-investigation attended")
    A363 = (20079, "A363", "Cancer Detected - Post-investigation Attended")
    A364 = (20227, "A364", "Cancer Detected - Post-investigation Not Required")
    A365 = (20228, "A365", "Refer Surgery - Post-investigation Not Required")
    A37 = (
        11123,
        "A37",
        "Patient Discharge Sent (Non-attendance at Colonoscopy Assessment Appointment)",
    )
    A370 = (160161, "A370", "Diagnostic Test Result Letter sent to GP")
    A371 = (20080, "A371", "Surgery Patient Result letter Printed")
    A372 = (20081, "A372", "Refer Symptomatic, GP Letter Printed")
    A373 = (305780, "A373", "Symptomatic result recorded")
    A374 = (20082, "A374", "Return to Surveillance After Symptomatic Referral")
    A375 = (
        160176,
        "A375",
        "Diagnostic Test Result Patient Letter Printed - Post-investigation Clinic List",
    )
    A376 = (20430, "A376", "Polyps not cancer, return to screening")
    A377 = (305701, "A377", "Return to Lynch after symptomatic referral")
    A38 = (11124, "A38", "Decision not to Continue with Diagnostic Test")
    A380 = (160164, "A380", "Failed Diagnostic Test - Refer Another")
    A382 = (11553, "A382", "Handover into Symptomatic Care - GP Letter Printed")
    A383 = (20421, "A383", "Handover into Symptomatic Care - Patient Letter Printed")
    A384 = (20420, "A384", "Discharged from Screening - GP letter not required")
    A385 = (20419, "A385", "Handover into Symptomatic Care")
    A389 = (
        305783,
        "A389",
        "Refer Another Diagnostic Test after return from Symptomatic Referral",
    )
    A391 = (20083, "A391", "Patient Discharge Letter Printed - No Patient Contact")
    A392 = (20084, "A392", "Patient Discharge Letter Printed - Patient Choice")
    A394 = (
        20418,
        "A394",
        "Handover into Symptomatic Care for Surveillance - Patient Age",
    )
    A395 = (160188, "A395", "Refer Another Diagnostic Test")
    A396 = (160165, "A396", "Discharged  from Screening Round - Patient Choice")
    A397 = (160167, "A397", "Discharged  from Screening Round - No Patient Contact")
    A400 = (160207, "A400", "Follow-up Test Cancelled by Screening Centre")
    A401 = (160208, "A401", "Patient Declined Follow-up Test")
    A402 = (160209, "A402", "Diagnostic Test Outcome Entered")
    A403 = (160229, "A403", "Reschedule Follow-up Test as Surveillance")
    A404 = (11104, "A404", "Changed Diagnostic Test Data")
    A410 = (160173, "A410", "Post-investigation Appointment Made")
    A415 = (160175, "A415", "Post-investigation Appointment Invitation Letter Printed")
    A416 = (160210, "A416", "Post-investigation Appointment Attended")
    A417 = (160177, "A417", "Post-investigation Appointment Cancelled by SC")
    A420 = (160178, "A420", "Post-investigation Appointment Cancelled by Patient")
    A422 = (
        160181,
        "A422",
        "Post-investigation Appointment Cancellation Letter Printed",
    )
    A425 = (
        160179,
        "A425",
        "Practitioner did not attend Post-investigation Appointment",
    )
    A430 = (
        160189,
        "A430",
        "Post-investigation Appointment Attended - Diagnostic Result Letter not Printed",
    )
    A441 = (160180, "A441", "Patient did not attend Post-investigation Appointment")
    A45 = (11125, "A45", "Weak Positive (Weak Positive)")
    A50 = (305489, "A50", "Diagnosis date recorded")
    A51 = (305498, "A51", "Diagnosis date amended")
    A52 = (305499, "A52", "No diagnosis date recorded")
    A59 = (11126, "A59", "Invited for Diagnostic Test")
    A60 = (11127, "A60", "Decision not to Continue with Other Tests")
    A61 = (160211, "A61", "Consent Withdrawn Diagnostic Test - Result Letter Printed")
    A62 = (160184, "A62", "Low-risk Adenoma")
    A63 = (160170, "A63", "Cancer")
    A64 = (160186, "A64", "High-risk Adenoma")
    A65 = (160187, "A65", "Abnormal/No Result")
    A8 = (11132, "A8", "Abnormal")
    A85 = (11133, "A85", "Waiting for Clinician Review")
    A99 = (11136, "A99", "Suitable for Endoscopic Test")
    ADHOCLETT = (11137, "ADHOCLETT", "Individual Letter")
    ANY = (11138, "ANY*", "Any Event Code")
    ANY_IF_NOT_CLOSED = (
        11295,
        "ANY_IF_NOT_CLOSED*",
        "Any Event Status if Episode is not Closed",
    )
    ANY_IF_OPEN = (11294, "ANY_IF_OPEN*", "Any Event Status if Episode is Open")
    ANY_OR_NO_EPI = (15005, "ANY_OR_NO_EPI*", "Any Event Code")
    C1 = (35, "C1", "Manual Cease Requested (Disclaimer Letter Required)")
    C10 = (40, "C10", "Manual Cease Request Removed")
    C11 = (41, "C11", "Manual Cease Requested (Immediate Cease)")
    C2 = (36, "C2", "Disclaimer Letter Marked as Sent")
    C203 = (11288, "C203", "Episode Closed")
    C4 = (
        37,
        "C4",
        "Receipt of Returned Disclaimer Letter Recorded - Manual Cease Confirmed",
    )
    C5 = (
        38,
        "C5",
        "Receipt of Returned Disclaimer Letter Recorded - Manual Do Not Cease Confirmed",
    )
    C9 = (39, "C9", "Uncease After Manual Cease")
    ContinueFromPending = (11287, "ContinueFromPending", "Continue from Pending")
    DUMMY = (
        11296,
        "DUMMY",
        "Pseudo Event Status created to allow Event Transition Processing to work",
    )
    E73 = (209020, "E73", "Reopen to book a bowel scope appointment for a correction")
    E74 = (
        205009,
        "E74",
        "Reopen to book a bowel scope appointment following subject decision",
    )
    E75 = (
        209017,
        "E75",
        "Reopen bowel scope Screening episode after Returned/Undelivered Mail",
    )
    E76 = (209018, "E76", "Print Returned/Undelivered mail letter")
    E79 = (
        209019,
        "E79",
        "Automatic Reopen bowel scope Screening episode after Returned/Undelivered Mail",
    )
    F1 = (200650, "F1", "Selected for bowel scope Screening")
    F10 = (200652, "F10", "Bowel scope Screening Invitation and appointment sent")
    F100 = (
        208068,
        "F100",
        "Unable to contact subject to complete bowel scope Suitability Assessment (GP) letter sent",
    )
    F11 = (200654, "F11", "Selected for bowel scope Screening Reminder")
    F12 = (200655, "F12", "Bowel scope Screening Reminder sent")
    F13 = (
        200656,
        "F13",
        "Bowel scope Appointment Invitation Sent (Subject not responded yet)",
    )
    F14 = (200657, "F14", "Bowel scope Screening Non-Response Sent")
    F15 = (209009, "F15", "Selected for bowel scope Screening Non-Response")
    F16 = (209010, "F16", "Bowel scope Screening Non-Response sent")
    F172 = (206040, "F172", "DNA bowel scope")
    F173 = (206041, "F173", "Subject Discharge Letter Printed - DNA bowel scope")
    F174 = (206042, "F174", "GP Discharge Letter Printed - DNA bowel scope")
    F175 = (203157, "F175", "Subject DNA bowel scope")
    F18 = (
        206010,
        "F18",
        "Bowel scope Appointment Cancelled by Screening Centre (prior to issue)",
    )
    F19 = (
        206011,
        "F19",
        "Bowel scope List Cancelled by Screening Centre (prior to issue)",
    )
    F199 = (203024, "F199", "Refer Colonoscopy")
    F2 = (206000, "F2", "Initial bowel scope appointment linked to episode")
    F20 = (206043, "F20", "Responded to bowel scope Screening Invitation")
    F200 = (203022, "F200", "Colonoscopy Assessment Appointment Required")
    F201 = (205044, "F201", "Colonoscopy Assessment Appointment Requested")
    F202 = (
        205045,
        "F202",
        "Colonoscopy Assessment Appointment Requested following DNA",
    )
    F203 = (205046, "F203", "2nd Colonoscopy Assessment Appointment Non Attendance")
    F204 = (
        205047,
        "F204",
        "Colonoscopy Assessment Appointment Non-attendance (Patient)",
    )
    F205 = (
        205048,
        "F205",
        "Colonoscopy Assessment Appointment Requested (Screening Centre Cancellation Letter)",
    )
    F206 = (
        205049,
        "F206",
        "Colonoscopy Assessment Appointment Cancellation (Screening Centre)",
    )
    F207 = (
        205050,
        "F207",
        "Colonoscopy Assessment Appointment Requested (Patient to Reschedule Letter)",
    )
    F208 = (
        205051,
        "F208",
        "Colonoscopy Assessment Appointment Cancellation Sent (Patient to Consider)",
    )
    F209 = (
        205052,
        "F209",
        "Colonoscopy Assessment Appointment Non-attendance Letter Sent (Patient)",
    )
    F21 = (
        206012,
        "F21",
        "Bowel scope Appointment Cancelled by Screening Centre (Confirmed)",
    )
    F210 = (
        205053,
        "F210",
        "Colonoscopy Assessment Appointment Non-attendance (Screening Centre)",
    )
    F212 = (
        205054,
        "F212",
        "Colonoscopy Assessment Appointment Requested (Screening Centre Non-attendance Letter)",
    )
    F213 = (
        205055,
        "F213",
        "Colonoscopy Assessment Appointment Cancellation (Patient to Consider Letter)",
    )
    F214 = (205056, "F214", "Colonoscopy Assessment Appointment Cancellation (Patient)")
    F215 = (
        205057,
        "F215",
        "Patient Discharge Sent (Non-attendance at Colonoscopy Assessment Appointment)",
    )
    F216 = (205058, "F216", "Colonoscopy Assessment Appointment Booked, letter sent")
    F217 = (
        205059,
        "F217",
        "Colonoscopy Assessment Appointment Booked following DNA, letter sent",
    )
    F218 = (
        205060,
        "F218",
        "GP Discharge Sent (Non-attendance at Colonoscopy Assessment Appointment)",
    )
    F219 = (
        205061,
        "F219",
        "Colonoscopy Assessment Appointment Cancellation Requested by Screening Centre prior to Preparation of Letter",
    )
    F22 = (
        206013,
        "F22",
        "Bowel scope Appointment Cancelled by Screening Centre (Not Responded Yet)",
    )
    F220 = (205062, "F220", "Colonoscopy Assessment Appointment Request (Redirected)")
    F221 = (205063, "F221", "Colonoscopy Assessment Appointment Requested (Redirected)")
    F222 = (204311, "F222", "GP Abnormal Result Created (Referred for Colonoscopy)")
    F223 = (205064, "F223", "Colonoscopy Assessment Appointment Rescheduled")
    F224 = (
        205065,
        "F224",
        "Patient Discharge Sent (Refused Colonoscopy Assessment Appointment)",
    )
    F225 = (
        205066,
        "F225",
        "GP Discharge Letter Sent (Refused Colonoscopy Assessment Appointment)",
    )
    F227 = (
        205067,
        "F227",
        "Post-investigation not Colonoscopy Assessment Appointment Required - letter to patient",
    )
    F228 = (204312, "F228", "GP Abnormal Result Created")
    F229 = (204258, "F229", "GP Abnormal Result Sent")
    F23 = (206014, "F23", "Bowel scope Appointment Re-allocated by Screening Centre")
    F24 = (206015, "F24", "Bowel scope Appointment Cancelled by Subject (Confirmed)")
    F25 = (206016, "F25", "Bowel scope Appointment Cancelled by Subject (Responded)")
    F26 = (
        206017,
        "F26",
        "Bowel scope Appointment Cancelled by Screening Centre (Responded)",
    )
    F27 = (206018, "F27", "Bowel scope List Cancelled by Screening Centre (Confirmed)")
    F28 = (206019, "F28", "Bowel scope List Cancelled by Screening Centre (Responded)")
    F29 = (
        206020,
        "F29",
        "Bowel scope List Cancelled by Screening Centre (Not Responded Yet)",
    )
    F30 = (206021, "F30", "Bowel scope Appointment Booked")
    F31 = (206022, "F31", "Bowel scope Appointment Booked (Invitation Sent)")
    F317 = (202064, "F317", "No Post-Investigation Contact Made")
    F32 = (209011, "F32", "Bowel scope Appointment Confirmed")
    F33 = (208043, "F33", "Bowel scope Appointment Confirmed (with Letter)")
    F34 = (204025, "F34", "Bowel scope Appointment Confirmation Letter Printed")
    F35 = (206023, "F35", "Bowel scope Appointment Booked (Following SC Cancellation)")
    F36 = (
        209012,
        "F36",
        "Bowel scope Appointment Booked (Another Appointment Required)",
    )
    F37 = (206024, "F37", "Bowel scope Appointment Booked (Screening Centre Rebook)")
    F38 = (206025, "F38", "Bowel scope Appointment Booked (Subject Not Responded Yet)")
    F39 = (206026, "F39", "Bowel scope Appointment Booked (Subject Rebook)")
    F40 = (206027, "F40", "Bowel scope Appointment Cancelled (Non Response)")
    F41 = (205024, "F41", "Subject letter for Non response Sent")
    F42 = (205025, "F42", "GP letter for Non-response Sent")
    F45 = (205026, "F45", "Bowel scope Bowel Prep Requested")
    F46 = (205027, "F46", "Bowel scope Bowel Prep Sent")
    F47 = (203156, "F47", "Screening Centre DNA bowel scope")
    F50 = (206028, "F50", "Bowel scope Appointment Cancelled (Manual Cancellation)")
    F51 = (
        206029,
        "F51",
        "Bowel scope Appointment Cancellation Letter Sent (Manual cancellation)",
    )
    F52 = (205139, "F52", "Bowel scope Appointment Cancelled (Subject not available)")
    F53 = (
        208093,
        "F53",
        "Bowel scope Appointment Re-allocated (Subject Not Responded Yet)",
    )
    F54 = (208094, "F54", "Bowel scope Appointment Re-allocated (prior to issue)")
    F55 = (
        205140,
        "F55",
        "Bowel scope Appointment Cancelled (Insufficient availability)",
    )
    F60 = (206030, "F60", "Bowel scope Appointment Cancelled (Not Suitable)")
    F69 = (203023, "F69", "Book another bowel scope Appointment")
    F70 = (
        206031,
        "F70",
        "Another bowel scope Screening Appointment Required following investigation",
    )
    F71 = (
        206032,
        "F71",
        "Another bowel scope Screening Appointment Required (Not Responded Yet)",
    )
    F710 = (205068, "F710", "Colonoscopy Assessment Appointment Attended")
    F711 = (
        205069,
        "F711",
        "Post-investigation Appointment Attended as Post-investigation",
    )
    F712 = (202078, "F712", "Colonoscopy Assessment Appointment Attended")
    F713 = (202079, "F713", "Colonoscopy Assessment Dataset Not Completed")
    F714 = (202080, "F714", "Colonoscopy Assessment Complete")
    F715 = (
        202095,
        "F715",
        "Result Letter on Queue (No colonoscopy assessment appointment)",
    )
    F716 = (
        202096,
        "F716",
        "Result Letter on Queue (Colonoscopy assessment appointment attended)",
    )
    F717 = (
        204314,
        "F717",
        "GP Result Communication Created (Colonoscopy assessment appointment attended)",
    )
    F718 = (
        204315,
        "F718",
        "GP Result Communication Created (No colonoscopy assessment appointment)",
    )
    F719 = (
        204316,
        "F719",
        "Patient Result Letter Created (No colonoscopy assessment appointment)",
    )
    F72 = (206033, "F72", "Another bowel scope Screening Appointment Required (Misc)")
    F720 = (
        204317,
        "F720",
        "Patient Result Letter Created (Colonoscopy assessment appointment attended)",
    )
    F73 = (206034, "F73", "Bowel scope Appointment Booked (Following Investigation)")
    F74 = (206035, "F74", "Bowel scope Appointment Booked (Misc)")
    F75 = (206036, "F75", "Bowel scope Appointment Booked (Subject Not Responded Yet)")
    F76 = (
        204043,
        "F76",
        "Close bowel scope episode on Decline, prepare subject letter",
    )
    F77 = (
        206037,
        "F77",
        "Subject not available for offered appointment, prepare subject letter",
    )
    F78 = (
        206038,
        "F78",
        "Bowel scope Appointment Cancelled (Insufficient Availability)",
    )
    F79 = (204044, "F79", "Close bowel scope episode on Decline, prepare GP letter")
    F80 = (
        204045,
        "F80",
        "Subject not available for offered appointment, prepare GP letter",
    )
    F81 = (
        204046,
        "F81",
        "Close bowel scope episode on Opt out of current episode, prepare patient letter",
    )
    F82 = (
        204047,
        "F82",
        "Close bowel scope episode on Opt out of current episode, prepare GP letter",
    )
    F83 = (205000, "F83", "Self-referred for bowel scope Screening")
    F84 = (206039, "F84", "Bowel scope Appointment Booked (Self-refer)")
    F85 = (
        209013,
        "F85",
        "Subject not available for offered appointment, GP letter printed",
    )
    F86 = (205028, "F86", "Bowel scope Appointment Booked (Self-referral)")
    F87 = (
        205029,
        "F87",
        "Bowel scope Appointment Confirmed (Self-referral with Letter)",
    )
    F88 = (
        203181,
        "F88",
        "Close bowel scope episode due to incorrect date of birth, prepare subject letter",
    )
    F9 = (200651, "F9", "Bowel scope Screening Pre-invitation sent")
    F92 = (205001, "F92", "Close bowel scope screening episode")
    F93 = (209016, "F93", "Request Returned/undelivered mail letter")
    F95 = (208063, "F95", "Assessed NOT suitable for bowel scope")
    F96 = (208064, "F96", "Assessed NOT suitable for bowel scope (subject) letter sent")
    F97 = (208065, "F97", "Assessed NOT suitable for bowel scope (GP) letter sent")
    F98 = (
        208066,
        "F98",
        "Unable to contact subject to complete BS Suitability Assessment",
    )
    F99 = (
        208067,
        "F99",
        "Unable to contact subject to complete bowel scope Suitability Assessment (subject) letter sent",
    )
    G1 = (307067, "G1", "Selected for Lynch Surveillance (Prevalent)")
    G2 = (307068, "G2", "Lynch Pre-invitation Sent")
    G3 = (305634, "G3", "Lynch Surveillance Assessment Appointment Required")
    G4 = (307126, "G4", "Selected for Lynch Surveillance (Self-referral)")
    G5 = (307076, "G5", "Selected for Lynch Surveillance (Incident)")
    G6 = (307081, "G6", "Review suitability for Lynch Surveillance")
    G7 = (307085, "G7", "Not suitable for Lynch Surveillance (Recent Colonoscopy)")
    G8 = (
        307095,
        "G8",
        "Not suitable for Lynch Surveillance (Recent Colonoscopy) patient letter sent",
    )
    G9 = (307086, "G9", "Not suitable for Lynch Surveillance (Incorrect Diagnosis)")
    G10 = (
        307096,
        "G10",
        "Not suitable for Lynch Surveillance (Incorrect Diagnosis) patient letter sent",
    )
    G11 = (
        307097,
        "G11",
        "Not suitable for Lynch Surveillance (Incorrect Diagnosis) GP letter sent",
    )
    G12 = (307102, "G12", "Not suitable for Lynch Surveillance (Clinical Reason)")
    G13 = (
        307103,
        "G13",
        "Not suitable for Lynch Surveillance (Clinical Reason) patient letter sent",
    )
    G14 = (
        307104,
        "G14",
        "Not suitable for Lynch Surveillance (Clinical Reason) GP letter sent",
    )
    G92 = (305691, "G92", "Close Lynch Episode via Interrupt")
    J1 = (202465, "J1", "Subsequent Assessment Appointment Required")
    J10 = (11139, "J10", "Attended Colonoscopy Assessment Appointment")
    J11 = (
        11140,
        "J11",
        "1st Colonoscopy Assessment Appointment Non-attendance (Patient)",
    )
    J12 = (11141, "J12", "Appointment Cancelled following a DNA (Screening Centre)")
    J13 = (
        11142,
        "J13",
        "Appointment Cancelled following a DNA (Patient to Reschedule)",
    )
    J14 = (11143, "J14", "Appointment Cancelled following a DNA (Patient to Consider)")
    J15 = (11144, "J15", "Not Suitable for Diagnostic Tests")
    J16 = (11145, "J16", "Patient Discharge Sent (Unsuitable for Diagnostic Tests)")
    J17 = (11146, "J17", "GP Discharge Sent (Unsuitable for Diagnostic Tests)")
    J18 = (11147, "J18", "Appointment Requested (Screening Centre Cancellation Letter)")
    J19 = (
        11148,
        "J19",
        "Appointment Requested following a DNA (Screening Centre Cancel Letter)",
    )
    J2 = (11149, "J2", "Appointment Cancellation (Screening Centre)")
    J20 = (11150, "J20", "Appointment Requested (Patient to Reschedule Letter)")
    J21 = (
        11151,
        "J21",
        "Appointment Requested following a DNA (Patient to Reschedule Letter)",
    )
    J22 = (11152, "J22", "Appointment Cancellation letter sent (Patient to Consider)")
    J23 = (
        11153,
        "J23",
        "Appointment Cancellation letter sent following a DNA (Patient to Consider)",
    )
    J24 = (11154, "J24", "Screening Centre Discharge Patient")
    J25 = (11155, "J25", "Patient discharge sent (Screening Centre discharge patient)")
    J26 = (11156, "J26", "GP Discharge letter sent (Discharge by Screening centre)")
    J27 = (11157, "J27", "Appointment Non-attendance Letter Sent (Patient)")
    J28 = (11158, "J28", "Appointment Non-attendance (Screening Centre)")
    J29 = (
        11159,
        "J29",
        "Appointment Non-attendance following a DNA (Screening Centre)",
    )
    J3 = (11160, "J3", "Patient Refused Colonoscopy Assessment Appointment")
    J30 = (11161, "J30", "Appointment Requested (SC Non-attendance Letter)")
    J31 = (
        11162,
        "J31",
        "Appointment Requested following a DNA (SC Non-attendance Letter)",
    )
    J32 = (205214, "J32", "Colonoscopy Assessment Appointment Request (Redirected)")
    J33 = (205222, "J33", "Colonoscopy Assessment Appointment Requested (Redirected)")
    J34 = (305443, "J34", "Subsequent Appointment Requested")
    J35 = (305444, "J35", "Subsequent Appointment Booked, letter sent")
    J36 = (305445, "J36", "Subsequent Appointment Non-attendance (Patient)")
    J37 = (305446, "J37", "Subsequent Appointment Requested following a DNA")
    J38 = (305447, "J38", "Subsequent Appointment Booked, letter sent following a DNA")
    J4 = (11163, "J4", "Appointment Cancellation (Patient to Consider)")
    J40 = (
        305448,
        "J40",
        "Subsequent Appointment Non-attendance (Patient) following a DNA",
    )
    J5 = (11164, "J5", "Appointment Cancellation (Patient to Reschedule)")
    J7 = (202466, "J7", "Colonoscopy Assessment Dataset Completed")
    J8 = (
        11165,
        "J8",
        "Patient discharge sent (refused colonoscopy assessment appointment)",
    )
    J9 = (
        11166,
        "J9",
        "GP discharge letter sent (refusal of colonoscopy assessment appointment)",
    )
    K105 = (11167, "K105", "Waiting for Confirmation of Closure")
    K188 = (11168, "K188", "New Kit Requested")
    K189 = (11169, "K189", "New Kit Sent")
    L204 = (11291, "L204", "Letter Queued")
    L205 = (11292, "L205", "Communication Cancelled")
    L206 = (11297, "L206", "Supplementary Letter Printed")
    L207 = (11298, "L207", "Letter Reprinted")
    L208 = (11299, "L208", "Redundant Letter Printed")
    M1 = (305757, "M1", "NHS App message requested")
    N112 = (11170, "N112", "Test Spoilt (Weak Positive & Normal)")
    N113 = (11171, "N113", "Technical Fail (Weak Positive & Normal)")
    N114 = (11172, "N114", "Test Spoilt, Assistance Required (Weak Positive & Normal)")
    N115 = (11173, "N115", "Retest Kit Sent (Spoilt; Weak Positive & Normal)")
    N116 = (11174, "N116", "Retest Kit Sent (Assisted; Weak Positive & Normal)")
    N117 = (11175, "N117", "Retest Kit Sent (Technical Fail; Weak Positive & Normal)")
    N118 = (11176, "N118", "Kit Returned and Logged (Spoilt; Weak Positive & Normal)")
    N119 = (11177, "N119", "Kit Returned and Logged (Assisted; Weak Positive & Normal)")
    N120 = (
        11178,
        "N120",
        "Kit Returned and Logged (Technical Fail; Weak Positive & Normal)",
    )
    N121 = (
        11179,
        "N121",
        "Reminder of Retest Kit Sent (Spoilt; Weak Positive & Normal)",
    )
    N122 = (
        11180,
        "N122",
        "Reminder of Retest Kit Sent (Assisted; Weak Positive & Normal)",
    )
    N123 = (
        11181,
        "N123",
        "Reminder of Retest Kit Sent (Technical Fail; Weak Positive & Normal)",
    )
    N124 = (
        11182,
        "N124",
        "GP Discharge for Non-response Sent (Spoilt Retest Kit; Weak Positive & Normal)",
    )
    N125 = (
        11183,
        "N125",
        "GP Discharge for Non-response Sent (Assisted Retest Kit; Weak Positive & Normal)",
    )
    N126 = (
        11184,
        "N126",
        "GP Discharge for Non-response Sent (Technical Fail Retest Kit; Weak Positive & Normal)",
    )
    N129 = (11185, "N129", "Technical Fail (Weak Positive & Normal) (Spoilt History)")
    N137 = (
        11186,
        "N137",
        "Retest Kit Sent (Technical Fail; Weak Positive & Normal) (Spoilt History)",
    )
    N140 = (
        11187,
        "N140",
        "Kit Returned and Logged (Technical Fail; Weak Positive & Normal) (Spoilt History)",
    )
    N143 = (
        11188,
        "N143",
        "Reminder of Retest Kit Sent (Technical Fail; Weak Positive & Normal) (Spoilt History)",
    )
    N160 = (
        11189,
        "N160",
        "Weak Positive and One Normal, Waiting for Screening Centre Assistance",
    )
    N161 = (
        11190,
        "N161",
        "Weak Positive and One Normal, Waiting for Programme Hub Assistance",
    )
    N164 = (
        11191,
        "N164",
        "GP Discharge Sent (Non-acceptance of Assistance; Weak Positive & Normal)",
    )
    N174 = (
        11192,
        "N174",
        "GP Discharge for Non-response Sent (Technical Fail Retest Kit; Weak Positive & Normal) (Spoilt History)",
    )
    N179 = (11193, "N179", "Assisted (Weak Positive & Normal) New Kit Required")
    N182 = (11194, "N182", "Assisted (Weak Positive & Normal) No Response")
    P202 = (11195, "P202", "Waiting Completion of Spur Events")
    P300 = (160212, "P300", "Defer, Pending Further Assessment")
    P88 = (11196, "P88", "Waiting Further Information")
    Q0 = (160236, "Q0", "Selected for a 30 Day Questionnaire")
    Q1 = (
        160237,
        "Q1",
        "30 Day Questionnaire (Screening: Endoscopy only) letter created",
    )
    Q2 = (
        160238,
        "Q2",
        "30 Day Questionnaire (Screening: Endoscopy & Radiology) letter created",
    )
    Q208 = (160230, "Q208", "Discard Diagnostic Test")
    Q209 = (20239, "Q209", "30 Day Questionnaire printed")
    Q3 = (
        160239,
        "Q3",
        "30 Day Questionnaire (Screening: Radiology only) letter created",
    )
    Q4 = (
        160240,
        "Q4",
        "30 Day Questionnaire (Surveillance: Endoscopy only) letter created",
    )
    Q5 = (
        160241,
        "Q5",
        "30 Day Questionnaire (Surveillance: Endoscopy & Radiology) letter created",
    )
    Q6 = (
        160242,
        "Q6",
        "30 Day Questionnaire (Surveillance: Radiology only) letter created",
    )
    RedirectedWithinEpisode = (
        11286,
        "RedirectedWithinEpisode",
        "Redirected within Episode",
    )
    REPRODUCELETT = (11293, "REPRODUCELETT", "Re-produced Letter from Archive")
    S1 = (11197, "S1", "Selected for Screening")
    S10 = (11198, "S10", "Invitation & Test Kit Sent")
    S11 = (11199, "S11", "Retest Kit Sent (Spoilt)")
    S12 = (11200, "S12", "Retest Kit Sent (Assisted)")
    S127 = (11201, "S127", "Technical Fail (Spoilt History)")
    S13 = (11202, "S13", "Retest Kit Sent (Technical Fail)")
    S135 = (11203, "S135", "Retest Kit Sent (Technical Fail) (Spoilt History)")
    S138 = (11204, "S138", "Kit Returned and Logged (Technical Fail) (Spoilt History)")
    S141 = (
        11205,
        "S141",
        "Reminder of Retest Kit Sent (Technical Fail) (Spoilt History)",
    )
    S157 = (11206, "S157", "Pre-invitation Sent (Opt-in)")
    S158 = (11207, "S158", "Subject Discharge Sent (Normal)")
    S159 = (11208, "S159", "GP Discharge Sent (Normal)")
    S162 = (11209, "S162", "GP Discharge Sent (Non-acceptance of Assistance)")
    S175 = (
        11210,
        "S175",
        "GP Discharge for Non-response Sent (Technical Fail Retest Kit) (Spoilt History)",
    )
    S177 = (11211, "S177", "Assisted, New Kit Required")
    S180 = (11212, "S180", "Assisted, No Response")
    S19 = (11213, "S19", "Reminder of Initial Test Sent")
    S192 = (11214, "S192", "Subject Discharge Sent (Normal; Weak Positive)")
    S193 = (11215, "S193", "GP Discharge Sent (Normal; Weak Positive)")
    S195 = (200520, "S195", "Receipt of  Self-referral kit")
    S2 = (11216, "S2", "Normal")
    S20 = (11217, "S20", "Reminder of Retest Kit Sent (Spoilt)")
    S201 = (11218, "S201", "Follow Up Questionnaire Sent (Normal)")
    S21 = (11219, "S21", "Reminder of Retest Kit Sent (Assisted)")
    S22 = (11220, "S22", "Reminder of Retest Kit Sent (Technical Fail)")
    S23 = (306108, "S23", "Reminder of Retest Kit Sent (Screening Incident)")
    S24 = (306225, "S24", "Reminder of Replacement Kit Sent (Screening Incident)")
    S3 = (11221, "S3", "Test Spoilt")
    S4 = (11222, "S4", "Test Spoilt (Assistance Required)")
    S43 = (11223, "S43", "Kit Returned and Logged (Initial Test)")
    S44 = (11224, "S44", "GP Discharge for Non-response Sent (Initial Test")
    S46 = (11225, "S46", "Kit Returned and Logged (Spoilt")
    S47 = (11226, "S47", "GP Discharge for Non-response Sent (Spoilt Retest Kit")
    S49 = (11227, "S49", "Kit Returned and Logged (Assisted")
    S5 = (11228, "S5", "Technical Fail")
    S50 = (11229, "S50", "GP Discharge for Non-response Sent (Assisted Retest Kit")
    S51 = (
        11230,
        "S51",
        "GP Discharge for Non-response Sent (Technical Fail Retest Kit",
    )
    S52 = (11231, "S52", "Kit Returned and Logged (Technical Fail")
    S53 = (306107, "S53", "Kit Returned and Logged (Screening Incident")
    S54 = (
        306109,
        "S54",
        "GP Discharge for Non-response Sent (Screening Incident Retest",
    )
    S55 = (
        306193,
        "S55",
        "GP Discharge for Non-response Sent (Screening Incident Replacement",
    )
    S56 = (11232, "S56", "2nd Normal (Weak Positive & Normal")
    S61 = (160183, "S61", "Normal (No Abnormalities Found")
    S7 = (306104, "S7", "Result Invalidated (Screening Incident")
    S71 = (306106, "S71", "Retest Kit Sent (Screening Incident")
    S72 = (306105, "S72", "Test Kit Invalidated (Screening Incident")
    S73 = (306110, "S73", "Replacement Kit Sent (Screening Incident")
    S83 = (11234, "S83", "Selected for Screening (Self-referral")
    S84 = (11235, "S84", "Invitation and Test Kit Sent (Self-referral")
    S9 = (11236, "S9", "Pre-invitation Sent")
    S92 = (11237, "S92", "Close Screening Episode via Interrupt")
    S94 = (11238, "S94", "Selected for Screening (Opt-in")
    S95 = (11239, "S95", "Waiting for Screening Centre Assistance")
    S96 = (11240, "S96", "Waiting for Programme Hub Assistance")
    U128 = (11241, "U128", "Technical Fail (Weak Positive) (Spoilt History")
    U130 = (11242, "U130", "Normal (Weak Positive) (Spoilt History")
    U131 = (11243, "U131", "Weak Positive (Spoilt History")
    U132 = (11244, "U132", "Retest Kit Sent (Weak Positive & Normal) (Spoilt History")
    U133 = (
        11245,
        "U133",
        "Kit Returned and Logged (Weak Positive & Normal) (Spoilt History",
    )
    U134 = (
        11246,
        "U134",
        "Reminder of Retest Kit Sent (Weak Positive & Normal) (Spoilt History",
    )
    U136 = (
        11247,
        "U136",
        "Retest Kit Sent (Technical Fail; Weak Positive) (Spoilt History",
    )
    U139 = (
        11248,
        "U139",
        "Kit Returned and Logged (Technical Fail; Weak Positive) (Spoilt History",
    )
    U14 = (11249, "U14", "Retest Kit Sent (Weak Positive")
    U142 = (
        11250,
        "U142",
        "Reminder of Retest Kit Sent (Technical Fail; Weak Positive) (Spoilt History",
    )
    U144 = (11251, "U144", "Retest Kit Sent (Weak Positive) (Spoilt History")
    U145 = (11252, "U145", "Kit Returned and Logged (Weak Positive) (Spoilt History")
    U146 = (
        11253,
        "U146",
        "Reminder of Retest Kit Sent (Weak Positive) (Spoilt History",
    )
    U15 = (11254, "U15", "Retest Kit Sent (Weak Positive & Normal")
    U163 = (
        11255,
        "U163",
        "GP Discharge Sent (Non-acceptance of Assistance; Weak Positive",
    )
    U176 = (
        11256,
        "U176",
        "GP Discharge for Non-response Sent (Technical Fail Retest Kit; Weak Positive) (Spoilt History",
    )
    U178 = (11257, "U178", "Assisted (Weak Positive) New Kit Required")
    U181 = (11258, "U181", "Assisted (Weak Positive) No Response")
    U186 = (
        11259,
        "U186",
        "GP Discharge for Non-response Sent (Weak Positive Retest Kit) (Spoilt History",
    )
    U187 = (
        11260,
        "U187",
        "GP Discharge for Non-response Sent (Weak Positive & Normal Retest Kit) (Spoilt History",
    )
    U200 = (204106, "U200", "FIT Device Linked to Episode")
    U23 = (11261, "U23", "Reminder of Retest Kit Sent (Weak Positive")
    U24 = (11262, "U24", "Reminder of Retest Kit Sent (Weak Positive & Normal")
    U54 = (11263, "U54", "GP Discharge for Non-response Sent (Weak Positive Retest Kit")
    U55 = (11264, "U55", "Kit Returned and Logged (Weak Positive")
    U57 = (
        11265,
        "U57",
        "GP Discharge for Non-response Sent (Weak Positive & Normal Retest Kit",
    )
    U58 = (11266, "U58", "Kit Returned and Logged (Weak Positive & Normal")
    U6 = (11267, "U6", "Weak Positive")
    U66 = (11268, "U66", "Test Spoilt (Weak Positive")
    U67 = (11269, "U67", "Technical Fail (Weak Positive")
    U68 = (11270, "U68", "Test Spoilt, Assistance Required (Weak Positive")
    U69 = (11271, "U69", "Retest Kit (Spoilt; Weak Positive")
    U7 = (11272, "U7", "Normal (Weak Positive")
    U70 = (11273, "U70", "Reminder of Retest Kit Sent (Spoilt; Weak Positive")
    U71 = (
        11274,
        "U71",
        "GP Discharge for Non-response Sent (Spoilt Retest Kit; Weak Positive",
    )
    U72 = (11275, "U72", "Kit Returned and Logged (Spoilt; Weak Positive")
    U74 = (11276, "U74", "Kit Returned and Logged (Assisted; Weak Positive")
    U75 = (11277, "U75", "Retest Kit Sent (Assisted; Weak Positive")
    U76 = (11278, "U76", "Reminder of Retest Kit Sent (Assisted; Weak Positive")
    U77 = (
        11279,
        "U77",
        "GP Discharge for Non-response Sent (Assisted Retest Kit; Weak Positive",
    )
    U78 = (11280, "U78", "Retest Kit Sent (Technical Fail; Weak Positive")
    U79 = (11281, "U79", "Reminder of Retest Kit Sent (Technical Fail; Weak Positive")
    U80 = (
        11282,
        "U80",
        "GP Discharge for Non-response Sent (Technical Fail Retest Kit; Weak Positive",
    )
    U81 = (11283, "U81", "Kit Returned and Logged (Technical Fail; Weak Positive")
    U97 = (11284, "U97", "Weak Positive, Waiting for Screening Centre Assistance")
    U98 = (11285, "U98", "Weak Positive, Waiting for Programme Hub Assistance")

    def __init__(self, valid_value_id: int, allowed_value: str, description: str):
        """
        Initialize an EventStatusType enum member.

        Args:
            valid_value_id (int): The unique identifier for the event status.
            allowed_value (str): The event status code.
            description (str): The human-readable description of the event status.
        """
        self._id = valid_value_id
        self._code = allowed_value
        self._description = description

    @property
    def id(self) -> int:
        """
        Returns the unique identifier for the event status.

        Returns:
            int: The event status ID.
        """
        return self._id

    @property
    def code(self) -> str:
        """
        Returns the event status code.

        Returns:
            str: The event status code.
        """
        return self._code

    @property
    def description(self) -> str:
        """
        Returns the human-readable description of the event status.

        Returns:
            str: The description.
        """
        return self._description

    @classmethod
    def get_by_id(cls, id_: int) -> Optional["EventStatusType"]:
        """
        Returns the enum member matching the given id.

        Args:
            id_ (int): The event status ID to search for.

        Returns:
            Optional[EventStatusType]: The matching enum member, or None if not found.
        """
        return next((e for e in cls if e.id == id_), None)

    @classmethod
    def get_by_code(cls, code: str) -> Optional["EventStatusType"]:
        """
        Returns the enum member matching the given code.

        Args:
            code (str): The event status code to search for.

        Returns:
            Optional[EventStatusType]: The matching enum member, or None if not found.
        """
        return next((e for e in cls if e.code == code), None)

    @classmethod
    def get_by_description(cls, description: str) -> Optional["EventStatusType"]:
        """
        Returns the enum member matching the given description.

        Args:
            description (str): The event status description to search for.

        Returns:
            Optional[EventStatusType]: The matching enum member, or None if not found.
        """
        return next((e for e in cls if e.description == description), None)
