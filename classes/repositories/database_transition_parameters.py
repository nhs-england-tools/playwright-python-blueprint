from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class DatabaseTransitionParameters:
    """
    Data class for holding parameters for a database transition.
    """

    subject_id: Optional[int] = None
    event_id: Optional[int] = None
    key_id: Optional[int] = None
    appointment_inst_id: Optional[int] = None
    kit_id: Optional[int] = None
    transition_id: Optional[int] = None
    screening_status_reason_id: Optional[int] = None
    episode_status_reason_id: Optional[int] = None
    clinical_change_reason_id: Optional[int] = None
    notes: Optional[str] = None
    cease_date: Optional[date] = None
    diagnostic_test_proposed_date: Optional[date] = None
    diagnostic_test_confirmed_date: Optional[date] = None
    episode_closure_reason_id: Optional[int] = None
    user_id: Optional[int] = None
    rollback_on_failure: Optional[str] = None
    diagnostic_test_proposed_type_id: Optional[int] = None
    diagnostic_test_id: Optional[int] = None
    surgery_date: Optional[date] = None
    recall_interval: Optional[int] = None
    discharge_id: Optional[int] = None
    recall_calculation_method_id: Optional[int] = None
    recall_test_id: Optional[int] = None
    comms_initial_event_id: Optional[int] = None
    ecomm_lett_batch_record_id: Optional[int] = None
    ecomm_batch_letter_id: Optional[int] = None
    intended_extend_id: Optional[int] = None
    surgery_result_id: Optional[int] = None
    referral_type_id: Optional[int] = None
    additional_data_id1: Optional[int] = None
    additional_data_date1: Optional[date] = None

    def to_params_list(self) -> list:
        """
        Returns the parameters as a list in the order expected by the stored procedure.
        """
        return [
            self.subject_id,  # p_screening_subject_id
            self.event_id,  # p_event_id
            self.key_id,  # p_key_id
            self.appointment_inst_id,  # p_appointment_inst_id
            self.kit_id,  # p_kitid
            self.transition_id,  # p_event_transition_id
            self.screening_status_reason_id,  # p_ss_reason_for_change_id
            self.episode_status_reason_id,  # p_episode_status_reason_id
            self.clinical_change_reason_id,  # p_clinical_rsn_closure_id
            self.notes,  # p_notes
            self.cease_date,  # p_ceased_confirm_recd_date
            self.diagnostic_test_proposed_date,  # p_external_test_proposed_date
            self.diagnostic_test_confirmed_date,  # p_external_test_date
            self.episode_closure_reason_id,  # p_uncnfrmd_rsn_epis_close_id
            self.user_id,  # p_pio_id
            self.rollback_on_failure,  # p_rollback_on_failure
            self.diagnostic_test_proposed_type_id,  # p_proposed_type_id
            self.diagnostic_test_id,  # p_ext_test_id
            self.surgery_date,  # p_surgery_date
            self.recall_interval,  # p_alternative_scr_interval
            self.discharge_id,  # p_pd_id
            self.recall_calculation_method_id,  # p_recall_calculation_method_id
            self.recall_test_id,  # p_recall_ext_test_id
            self.comms_initial_event_id,  # p_comms_initial_event_id
            self.ecomm_lett_batch_record_id,  # p_ecomm_lett_batch_record_id
            self.ecomm_batch_letter_id,  # p_ecomm_batch_letter_id
            self.intended_extend_id,  # p_intended_extent_id
            self.surgery_result_id,  # p_surgery_result_id
            self.referral_type_id,  # p_screening_referral_type_id
            self.additional_data_id1,  # p_additional_data_id_1
            self.additional_data_date1,  # p_additional_data_date_1
            None,  # po_error_cur (OUT)
            None,  # po_data_cur (OUT)
        ]
