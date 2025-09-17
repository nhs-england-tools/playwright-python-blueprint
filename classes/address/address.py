from dataclasses import dataclass


@dataclass
class Address:
    """
    Represents a postal address with up to five address lines and a postcode.
    Provides methods to format the address as a string.
    """

    address_line1: str = ""
    address_line2: str = ""
    address_line3: str = ""
    address_line4: str = ""
    address_line5: str = ""
    post_code: str = ""

    def set_address_line(self, line_number: int, address_line: str) -> None:
        """
        Sets the specified address line (1-5) to the given value.

        Args:
            line_number (int): The address line number (1-5).
            address_line (str): The value to set for the address line.

        Raises:
            ValueError: If line_number is not between 1 and 5.
        """
        if not 1 <= line_number <= 5:
            raise ValueError(
                f"Invalid line number {line_number}, must be between 1 and 5"
            )

        setattr(self, f"address_line{line_number}", address_line)

    def __str__(self) -> str:
        """
        Returns the formatted address as a single string.
        """
        address_parts = [
            self.address_line1,
            self.address_line2,
            self.address_line3,
            self.address_line4,
            self.address_line5,
            self.post_code,
        ]
        return ", ".join([part for part in address_parts if part])
