from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class Analyser:
    """
    This data class is used to store information about a specific analyser device.
    The attributes correspond to the columns in the analyser query results.
    Attributes:
        analyser_id (Optional[int]): The ID of the analyser.
        analyser_code (Optional[str]): The code of the analyser.
        hub_id (Optional[int]): The ID of the hub the analyser is connected to.
        analyser_type_id (Optional[int]): The type ID of the analyser.
        spoil_result_code (Optional[int]): The result code for spoilage.
        tech_fail_result_code (Optional[int]): The result code for technical failure.
        below_range_result_code (Optional[int]): The result code for below range.
        above_range_result_code (Optional[int]): The result code for above range.
    """

    analyser_id: Optional[int] = None
    analyser_code: Optional[str] = None
    hub_id: Optional[int] = None
    analyser_type_id: Optional[int] = None
    spoil_result_code: Optional[int] = None
    tech_fail_result_code: Optional[int] = None
    below_range_result_code: Optional[int] = None
    above_range_result_code: Optional[int] = None

    def __str__(self) -> str:
        return (
            f"Analyser [analyser_id={self.analyser_id}, analyser_code={self.analyser_code}, "
            f"hub_id={self.hub_id}, spoil_result_code={self.spoil_result_code}, "
            f"tech_fail_result_code={self.tech_fail_result_code}, "
            f"below_range_result_code={self.below_range_result_code}, "
            f"above_range_result_code={self.above_range_result_code}]"
        )

    @staticmethod
    def from_dataframe_row(row: pd.Series) -> "Analyser":
        """
        Creates an Analyser object from a pandas DataFrame row containing analyser query results.

        Args:
            row (pd.Series): A row from a pandas DataFrame with columns:
                - tk_analyser_id
                - analyser_code
                - hub_id
                - tk_analyser_type_id
            The other columns are obtained from the SQL query as so are not present in this method.

        Returns:
            Analyser: The constructed Analyser object.
        """
        return Analyser(
            analyser_id=row.get("tk_analyser_id"),
            analyser_code=row.get("analyser_code"),
            hub_id=row.get("hub_id"),
            analyser_type_id=row.get("tk_analyser_type_id"),
        )
