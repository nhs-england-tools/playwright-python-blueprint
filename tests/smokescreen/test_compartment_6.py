import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.user_tools import UserTools
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.batch_processing import batch_processing
from pages.logout.log_out_page import LogoutPage
from pages.datasets.subject_datasets_page import SubjectDatasetsPage


# This should go into a util. Adding it here to avoid SonarQube duplication errors:
def go_to_investigation_datasets_page(page: Page, nhs_no) -> None:
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "A323 - Post-investigation Appointment NOT Required"
    )

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()


def investigation_dataset_forms(page: Page) -> None:
    page.locator("#UI_SITE_SELECT_LINK").click()
    page.locator("#UI_RESULTS_rljsjnkh").select_option("35317")
    page.locator("#UI_SSP_PIO_SELECT_LINK").click()
    page.locator("#UI_RESULTS_okdvpfko").select_option("1251")
    page.locator("#UI_CONSULTANT_PIO_SELECT_LINK").click()
    page.locator("#UI_RESULTS_sawaeghr").select_option("886")
    page.locator("#UI_ASPIRANT_ENDOSCOPIST_PIO_SELECT_LINK").click()
    page.locator("#anchorDrug").click()
    page.locator("#UI_BOWEL_PREP_DRUG1").select_option("200537~Tablet(s)")
    page.locator("#UI_BOWEL_PREP_DRUG_DOSE1").click()
    page.locator("#UI_BOWEL_PREP_DRUG_DOSE1").fill("10")
    page.get_by_role("link", name="Show details").click()
    page.locator("#radScopeInsertedYes").check()
    page.get_by_role("radio", name="Therapeutic").check()
    page.get_by_label("Bowel preparation quality").select_option("17016")
    page.get_by_label("Comfort during examination").select_option("18505")
    page.get_by_label("Comfort during recovery").select_option("18505")
    page.get_by_label("Endoscopist defined extent").select_option(
        "17240~Colonoscopy Complete"
    )
    page.get_by_label("Scope imager used").select_option("17058")
    page.get_by_label("Retroverted view").select_option("17059")
    page.get_by_role("textbox", name="Start of intubation time").click()
    page.get_by_role("textbox", name="Start of intubation time").fill("09:00")
    page.get_by_role("textbox", name="Start of extubation time").click()
    page.get_by_role("textbox", name="Start of extubation time").fill("09:15")
    page.get_by_role("textbox", name="End time of procedure").click()
    page.get_by_role("textbox", name="End time of procedure").fill("09:30")
    page.get_by_role("textbox", name="Scope ID").click()
    page.get_by_role("textbox", name="Scope ID").fill("A1")
    page.get_by_label("Insufflation").select_option("200547")
    page.get_by_label("Outcome at time of procedure").select_option(
        "17148~Complications are optional"
    )
    page.get_by_label("Late outcome").select_option(
        "17216~Complications are not required"
    )
    page.locator("#anchorCompletionProof").click()
    page.get_by_label("Proof Parameters").select_option("200575")


def investigation_datasets_failure_reason_and_adding_initial_polyp(page: Page) -> None:
    page.locator("#anchorFailure").click()
    page.get_by_label("Failure Reasons").select_option("205148")
    page.get_by_role("button", name="Add Polyp").click()
    page.locator("#UI_POLYP_LOCATION1").select_option("17240~Colonoscopy Complete")
    page.get_by_label("Classification ?").select_option("17295")
    page.get_by_role("textbox", name="Estimate of whole polyp size").click()


@pytest.mark.vpn_required
@pytest.mark.smokescreen
@pytest.mark.compartment5
def test_compartment_5(page: Page, smokescreen_properties: dict) -> None:
    """
    This is the main compartment 6 method
    Filling out the investigation datasets for different subjects to get different results for a diagnostic test.
    Printing the diagnostic test result letters.
    """

    # For the following tests old refers to if they are over 75 at recall
    # The recall period is 2 years from the last diagnostic test for a Normal or Abnormal diagnostic test result
    # or 3 years for someone who is going in to Surveillance (High-risk findings or LNPCP)

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # This needs to be repeated for two subjects, one old and one not - High Risk Result
    nhs_no = "9619187075"  # Dummy NHS Number (will not work)
    go_to_investigation_datasets_page(page, nhs_no)

    # The following code is on the investigation datasets page
    investigation_dataset_forms(page)
    investigation_datasets_failure_reason_and_adding_initial_polyp(page)
    page.get_by_role("textbox", name="Estimate of whole polyp size").fill("15")
    page.get_by_label("Polyp Access").select_option("17060")
    page.get_by_role("link", name="Add Intervention").click()
    page.locator("#UI_POLYP_THERAPY_MODALITY1_1").select_option("17189~Resection")
    page.locator("#UI_DEVICE1_1").select_option("17070")
    page.get_by_label("Excised").select_option("17058")
    page.get_by_label("Retrieved").select_option("17059")
    page.get_by_label("Excision Technique").select_option("17751")
    page.get_by_role("button", name="Add Polyp").click()
    page.locator("#UI_POLYP_LOCATION2").select_option("17239~Colonoscopy Complete")
    page.locator("#UI_POLYP_CLASS2").select_option("17295")
    page.locator("#UI_POLYP_SIZE2").click()
    page.locator("#UI_POLYP_SIZE2").fill("15")
    page.locator("#UI_POLYP_ACCESS2").select_option("17060")
    page.locator("#spanPolypInterventionLink2").get_by_role(
        "link", name="Add Intervention"
    ).click()
    page.locator("#UI_POLYP_THERAPY_MODALITY2_1").select_option("17193~Resection")
    page.locator("#UI_DEVICE2_1").select_option("17070")
    page.locator("#UI_POLYP_RESECTED2_1").select_option("17058")
    page.locator("#UI_POLYP_RETRIEVED2_1").select_option("17059")
    page.locator("#UI_POLYP_REMOVAL_TYPE2_1").select_option("17751")
    page.locator("#radDatasetCompleteYes").check()
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("#UI_DIV_BUTTON_SAVE1").get_by_role(
        "button", name="Save Dataset"
    ).click()

    expect(page.get_by_text("High-risk findings")).to_be_visible()
    BasePage(page).click_back_button()

    # The following code is on the subject datasets page
    expect(page.get_by_text("** Completed **").nth(1)).to_be_visible()
    BasePage(page).click_back_button()

    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Enter Diagnostic Test Outcome").click()
    # The following code is on the diagnostic test outcome page
    expect(page.get_by_role("cell", name="High-risk findings").nth(1)).to_be_visible()
    page.get_by_label("Outcome of Diagnostic Test").select_option("20365")
    page.get_by_role("button", name="Save").click()

    # This is if the subject is too old
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A394 - Handover into Symptomatic Care for Surveillance - Patient Age"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Handover into Symptomatic Care").click()

    # The following code is on the handover into symptomatic care page
    page.get_by_label("Referral").select_option("20445")
    page.get_by_role("button", name="Calendar").click()
    page.get_by_role(
        "cell", name="9", exact=True
    ).click()  # Todays date (v1 calendar picker)
    page.locator("#UI_NS_CONSULTANT_PIO_SELECT_LINK").click()
    page.locator("#UI_RESULTS_usgwmbob").select_option("201")
    page.locator("#UI_NS_PRACTITIONER_PIO_SELECT_LINK").click()
    page.get_by_role("textbox", name="Notes").click()
    page.get_by_role("textbox", name="Notes").fill("Test Automation")
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Save").click()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A385 - Handover into Symptomatic Care"
    )

    # This is if the subject is not too old
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Record Diagnosis Date").click()

    # The following code is on the record diagnosis date page
    page.locator("#diagnosisDate").click()
    page.locator("#diagnosisDate").fill("09 May 2025")  # Todays date
    page.get_by_role("button", name="Save").click()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )

    # This needs to be repeated for two subjects, one old and one not - LBPCP Result
    nhs_no = "9619187076"  # Dummy NHS Number (will not work)
    go_to_investigation_datasets_page(page, nhs_no)

    # The following code is on the investigation datasets page
    investigation_dataset_forms(page)
    investigation_datasets_failure_reason_and_adding_initial_polyp(page)
    page.get_by_role("textbox", name="Estimate of whole polyp size").fill("30")
    page.get_by_label("Polyp Access").select_option("17060")
    page.get_by_role("link", name="Add Intervention").click()
    page.locator("#UI_POLYP_THERAPY_MODALITY1_1").select_option("17189~Resection")
    page.locator("#UI_DEVICE1_1").select_option("17070")
    page.get_by_label("Excised").select_option("17058")
    page.get_by_label("Retrieved").select_option("17059")
    page.get_by_label("Excision Technique").select_option("17751")
    page.locator("#radDatasetCompleteYes").check()
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("#UI_DIV_BUTTON_SAVE1").get_by_role(
        "button", name="Save Dataset"
    ).click()

    expect(page.get_by_text("LNPCP")).to_be_visible()
    BasePage(page).click_back_button()

    # The following code is on the subject datasets page
    expect(page.get_by_text("** Completed **").nth(1)).to_be_visible()
    BasePage(page).click_back_button()

    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Enter Diagnostic Test Outcome").click()

    # The following code is on the diagnostic test outcome page
    expect(page.get_by_role("cell", name="LNPCP").nth(1)).to_be_visible()
    page.get_by_label("Outcome of Diagnostic Test").select_option("20365")
    page.get_by_role("button", name="Save").click()

    # If the subject is too old
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A394 - Handover into Symptomatic Care for Surveillance - Patient Age"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Handover into Symptomatic Care").click()

    # The following code is on the handover into symptomatic care page
    page.get_by_label("Referral").select_option("20445")
    page.get_by_role("button", name="Calendar").click()
    page.get_by_role(
        "cell", name="9", exact=True
    ).click()  # Todays date (v1 calendar picker)
    page.locator("#UI_NS_CONSULTANT_PIO_SELECT_LINK").click()
    page.locator("#UI_RESULTS_ktdtoepq").select_option("201")
    page.locator("#UI_NS_PRACTITIONER_PIO_SELECT_LINK").click()
    page.get_by_role("textbox", name="Notes").click()
    page.get_by_role("textbox", name="Notes").fill("Test Automation")
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Save").click()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A385 - Handover into Symptomatic Care"
    )

    # If the subject is not too old
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Record Diagnosis Date").click()

    # The following code is on the record diagnosis date page
    page.locator("#diagnosisDate").click()
    page.locator("#diagnosisDate").fill("09 May 2025")  # Todays date
    page.get_by_role("button", name="Save").click()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )

    # This needs to be repeated for 1 subject, age does not matter - Normal Result
    nhs_no = "9619187077"  # Dummy NHS Number (will not work)
    go_to_investigation_datasets_page(page, nhs_no)

    # The following code is on the investigation datasets page
    investigation_dataset_forms(page)
    page.locator("#anchorFailure").click()
    page.get_by_label("Failure Reasons").select_option("18500")
    page.locator("#radDatasetCompleteYes").check()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.locator("#UI_DIV_BUTTON_SAVE1").get_by_role(
        "button", name="Save Dataset"
    ).click()
    expect(page.get_by_text("Normal (No Abnormalities")).to_be_visible()
    BasePage(page).click_back_button()

    # The following code is on the subject datasets page
    expect(page.get_by_text("** Completed **").nth(1)).to_be_visible()
    BasePage(page).click_back_button()

    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Enter Diagnostic Test Outcome").click()

    # The following code is on the diagnostic test outcome page
    expect(
        page.get_by_role("cell", name="Normal (No Abnormalities").nth(1)
    ).to_be_visible()
    page.get_by_label("Outcome of Diagnostic Test").select_option("")
    page.get_by_label("Outcome of Diagnostic Test").select_option("20360")
    page.get_by_role("button", name="Save").click()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    page.get_by_role("button", name="Record Diagnosis Date").click()

    # The following code is on the record diagnosis date page
    page.locator("#diagnosisDate").click()
    page.locator("#diagnosisDate").fill("09 May 2025")  # Todays date
    page.get_by_role("button", name="Save").click()

    # Modification needs to be done to accept this list. it should check if any of the values in this list are present. Something like the following:
    # def get_first_visible_cell(page, values):
    # if isinstance(values, str):
    #     values = [values]
    # for name in values:
    #     locator = page.get_by_role("cell", name=name)
    #     if locator.is_visible():
    #         return locator

    batch_processing(
        page,
        "A318",
        "Result Letters - No Post-investigation Appointment",
        [
            "S61 - Normal (No Abnormalities Found)",
            "A158 - High-risk findings",
            "A157 - LNPCP",
        ],
    )

    batch_processing(
        page,
        "A385",
        "Handover into Symptomatic Care Adenoma Surveillance, Age - GP Letter",
        "A382 - Handover into Symptomatic Care - GP Letter Printed",
    )

    batch_processing(
        page,
        "A382",
        "Handover into Symptomatic Care Adenoma Surveillance - Patient Letter",
        "P202 - Waiting Completion of Outstanding Events",
    )

    LogoutPage(page).log_out()
