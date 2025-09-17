from utils.oracle.oracle import OracleDB
from classes.kits.analyser import Analyser
from classes.kits.analyser_result_code_type import AnalyserResultCodeType


class AnalyserRepository:
    """
    This class is responsible for analyzing and processing data related to FIT kits.
    """

    def __init__(self):
        self.oracle_db = OracleDB()

    def get_active_analyser_for_hub_and_kit_type(
        self, hub_id: int, kit_type: int
    ) -> "Analyser":
        """
        Fetches the active analyser for specific hubs and kit types

        Args:
            hub_id (int): The ID of the hub the user belongs to
            kit_type (int): The ID for the kit type

        Returns:
            Analyser: The analyser object
        """
        query = """
        SELECT DISTINCT
            tkan.tk_analyser_id,
            tkan.analyser_code,
            tkan.hub_id,
            tkan.tk_analyser_type_id
        FROM tk_analyser_t tkan
        INNER JOIN tk_analyser_type_t tkat
            ON tkat.tk_analyser_type_id = tkan.tk_analyser_type_id
        INNER JOIN tk_measurable_range tkmr
            ON tkmr.tk_analyser_type_id = tkat.tk_analyser_type_id
        WHERE TRUNC(SYSDATE) BETWEEN tkan.start_date AND NVL(tkan.end_date, SYSDATE)
            AND TRUNC(SYSDATE) BETWEEN tkmr.start_date AND NVL(tkmr.end_date, SYSDATE)
            AND tkan.hub_id = :hub_id
            AND tkmr.tk_type_id = :kit_type_id
        """
        params = {"hub_id": hub_id, "kit_type_id": kit_type}
        analyser_df = self.oracle_db.execute_query(query, params)
        return Analyser.from_dataframe_row(analyser_df.iloc[0])

    def get_spoilt_result_code(self, analyser_type_id: int) -> int:
        """
        Gets the Spoilt result code for the specified analyser type.
        Args:
            analyser_type_id (int): The ID of the analyser type.
        Returns:
            int: The Spoilt result code.
        """
        return self.get_result_code(analyser_type_id, AnalyserResultCodeType.SPOILT)

    def get_technical_fail_result_code(self, analyser_type_id: int) -> int:
        """
        Gets the Technical Fail result code for the specified analyser type.
        Args:
            analyser_type_id (int): The ID of the analyser type.
        Returns:
            int: The Technical Fail result code.
        """
        return self.get_result_code(
            analyser_type_id, AnalyserResultCodeType.TECHNICAL_FAIL
        )

    def get_result_code(
        self, analyser_type_id: int, result_code_type: "AnalyserResultCodeType"
    ) -> int:
        """
        Gets the result code for the specified analyser type and result code type from the database.
        Args:
            analyser_type_id (int): The ID of the analyser type.
            result_code_type (AnalyserResultCodeType): The type of result code.
        Returns:
            int: The result code for the specified analyser type and result code type
        """
        query = """
        SELECT
            tkte.tk_analyser_type_id,
            tkte.tk_analyser_error_type_id,
            tkte.error_code
        FROM tk_analyser_type_error tkte
        WHERE tkte.tk_analyser_type_id = :analyser_type_id
        AND tkte.tk_analyser_error_type_id = :code_type_id
        """
        params = {
            "analyser_type_id": int(analyser_type_id),
            "code_type_id": int(result_code_type.value[0]),
        }

        result_code_df = self.oracle_db.execute_query(query, params)
        if result_code_df.empty:
            raise ValueError(
                f"No result code found for analyser type id: {analyser_type_id} and code type id {result_code_type}"
            )
        return int(result_code_df["error_code"].iloc[0])
