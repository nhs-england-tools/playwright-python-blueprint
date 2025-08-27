from typing import Optional, Tuple, List


class DatabaseError:
    """
    Data class representing the error cursor normally returned as the first cursor in a stored procedure call.
    """

    def __init__(
        self,
        error_id: Optional[int] = None,
        field: Optional[str] = None,
        message_type: Optional[str] = None,
        return_message: Optional[str] = None,
        severity: Optional[int] = None,
        advice: Optional[str] = None,
    ) -> None:
        self.error_id: Optional[int] = error_id
        self.field: Optional[str] = field
        self.message_type: Optional[str] = message_type
        self.return_message: Optional[str] = return_message
        self.severity: Optional[int] = severity
        self.advice: Optional[str] = advice

    def get_error_id(self) -> Optional[int]:
        """
        Returns the error ID.
        """
        return self.error_id

    def set_error_id(self, error_id: int) -> None:
        """
        Sets the error ID.
        """
        self.error_id = error_id

    def get_field(self) -> Optional[str]:
        """
        Returns the field associated with the error.
        """
        return self.field

    def set_field(self, field: str) -> None:
        """
        Sets the field associated with the error.
        """
        self.field = field

    def get_message_type(self) -> Optional[str]:
        """
        Returns the message type.
        """
        return self.message_type

    def set_message_type(self, message_type: str) -> None:
        """
        Sets the message type.
        """
        self.message_type = message_type

    def get_return_message(self) -> Optional[str]:
        """
        Returns the return message.
        """
        return self.return_message

    def set_return_message(self, return_message: str) -> None:
        """
        Sets the return message.
        """
        self.return_message = return_message

    def get_advice(self) -> Optional[str]:
        """
        Returns the advice.
        """
        return self.advice

    def set_advice(self, advice: str) -> None:
        """
        Sets the advice.
        """
        self.advice = advice

    def get_severity(self) -> Optional[int]:
        """
        Returns the severity.
        """
        return self.severity

    def set_severity(self, severity: int) -> None:
        """
        Sets the severity.
        """
        self.severity = severity

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
