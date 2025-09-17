from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class DatabaseError:
    """
    Data class representing the error cursor normally returned as the first cursor in a stored procedure call.
    """

    error_id: Optional[int] = None
    field: Optional[str] = None
    message_type: Optional[str] = None
    return_message: Optional[str] = None
    severity: Optional[int] = None
    advice: Optional[str] = None

    def is_error(self) -> bool:
        """
        Returns True if this represents an error, otherwise False.
        """
        return self.error_id != 0

    @classmethod
    def from_cursor(cls, rows: List[Tuple]) -> "DatabaseError":
        """
        Map the first row of the error cursor into a DatabaseError instance.
        Expects cursor rows in the order:
            (error_id, field, message_type, return_message, severity, advice)
        """
        if not rows:
            return cls()  # no error row

        row = rows[0]
        return cls(
            error_id=row[0],
            field=row[1],
            message_type=row[2],
            return_message=row[3],
            severity=row[4],
            advice=row[5],
        )
