from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime
from utils.date_time_utils import DateTimeUtils


@dataclass
class KitServiceManagementRecord:
    """
    Data class representing a kit service management record.
    """

    # Kit queue data items
    device_id: Optional[str] = None
    test_kit_type: Optional[int] = None
    test_kit_name: Optional[str] = None
    test_kit_status: Optional[str] = None
    logged_by_hub: Optional[str] = None
    date_time_logged: Optional[datetime] = None
    test_result: Optional[Decimal] = None
    calculated_result: Optional[str] = None
    error_code: Optional[int] = None
    analyser_code: Optional[str] = None
    date_time_authorised: Optional[datetime] = None
    authoriser_user_code: Optional[str] = None
    datestamp: Optional[datetime] = None
    bcss_error_id: Optional[int] = None
    post_response: Optional[int] = None
    post_attempts: Optional[int] = None
    put_response: Optional[int] = None
    put_attempts: Optional[int] = None
    date_time_error_archived: Optional[datetime] = None
    error_archived_user_code: Optional[str] = None

    # Kit data items
    date_time_issued: Optional[datetime] = None
    issued_by_hub: Optional[str] = None
    nhs_number: Optional[str] = None
    analyser_error_description: Optional[str] = None
    error_type: Optional[str] = None
    screening_test_result: Optional[str] = None

    def __str__(self) -> str:
        return (
            f"KitServiceManagementRecord [device_id={self.device_id}, test_kit_type={self.test_kit_type}, \n"
            f"test_kit_name={self.test_kit_name}, test_kit_status={self.test_kit_status}, \n"
            f"logged_by_hub={self.logged_by_hub}, date_time_logged={self.date_time_logged}, \n"
            f"test_result={self.test_result}, calculated_result={self.calculated_result}, \n"
            f"error_code={self.error_code}, analyser_code={self.analyser_code}, \n"
            f"date_time_authorised={self.date_time_authorised}, authoriser_user_code={self.authoriser_user_code}, \n"
            f"datestamp={self.datestamp}, bcss_error_id={self.bcss_error_id}, post_response={self.post_response}, \n"
            f"post_attempts={self.post_attempts}, put_response={self.put_response}, put_attempts={self.put_attempts}, \n"
            f"date_time_error_archived={self.date_time_error_archived}, error_archived_user_code={self.error_archived_user_code}, \n"
            f"date_time_issued={self.date_time_issued}, issued_by_hub={self.issued_by_hub}, nhs_number={self.nhs_number}, \n"
            f"analyser_error_description={self.analyser_error_description}, error_type={self.error_type}, \n"
            f"screening_test_result={self.screening_test_result}]"
        )

    @staticmethod
    def from_dataframe_row(row) -> "KitServiceManagementRecord":
        """
        Creates a KitServiceManagementRecord object from a pandas DataFrame row containing kit service management query results.

        Args:
            row (pd.Series): A row from a pandas DataFrame with columns matching the query.

        Returns:
            KitServiceManagementRecord:  A populated KitServiceManagementRecord object from the given DataFrame row.
        """

        def parse_decimal(value):
            if value is None or value == "":
                return None
            try:
                return Decimal(str(value))
            except Exception:
                return None

        return KitServiceManagementRecord(
            device_id=row.get("device_id"),
            test_kit_type=row.get("test_kit_type"),
            test_kit_name=row.get("test_kit_name"),
            test_kit_status=row.get("test_kit_status"),
            logged_by_hub=row.get("logged_by_hub"),
            date_time_logged=DateTimeUtils.parse_datetime(row.get("date_time_logged")),
            test_result=parse_decimal(row.get("test_result")),
            calculated_result=row.get("calculated_result"),
            error_code=row.get("error_code"),
            analyser_code=row.get("analyser_code"),
            date_time_authorised=DateTimeUtils.parse_datetime(
                row.get("date_time_authorised")
            ),
            authoriser_user_code=row.get("authoriser_user_code"),
            datestamp=DateTimeUtils.parse_datetime(row.get("datestamp")),
            bcss_error_id=row.get("bcss_error_id"),
            post_response=row.get("post_response"),
            post_attempts=row.get("post_attempts"),
            put_response=row.get("put_response"),
            put_attempts=row.get("put_attempts"),
            date_time_error_archived=DateTimeUtils.parse_datetime(
                row.get("date_time_error_archived")
            ),
            error_archived_user_code=row.get("error_archived_user_code"),
            date_time_issued=DateTimeUtils.parse_datetime(row.get("issue_date")),
            issued_by_hub=row.get("issued_by_hub"),
            nhs_number=row.get("subject_nhs_number"),
            analyser_error_description=row.get("analyser_error_description"),
            error_type=row.get("error_type"),
            screening_test_result=row.get("test_results"),
        )
