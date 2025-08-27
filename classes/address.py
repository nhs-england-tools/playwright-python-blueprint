import logging


class Address:
    """
    Represents a postal address with up to five address lines and a postcode.
    Provides methods to set individual lines and to format the address as a string.
    """

    def __init__(self) -> None:
        self.address_line1: str = ""
        self.address_line2: str = ""
        self.address_line3: str = ""
        self.address_line4: str = ""
        self.address_line5: str = ""
        self.post_code: str = ""

    def set_address_line(self, line_number: int, address_line: str) -> None:
        """
        Sets the specified address line (1-5) to the given value.

        Args:
            line_number (int): The address line number (1-5).
            address_line (str): The value to set for the address line.

        Raises:
            ValueError: If line_number is not between 1 and 5.
        """
        logging.info(
            f"start: set_address_line(line_number={line_number}, address_line={address_line})"
        )
        if line_number == 1:
            self.address_line1 = address_line
        elif line_number == 2:
            self.address_line2 = address_line
        elif line_number == 3:
            self.address_line3 = address_line
        elif line_number == 4:
            self.address_line4 = address_line
        elif line_number == 5:
            self.address_line5 = address_line
        else:
            raise ValueError(
                f"Invalid line number {line_number}, must be between 1 and 5"
            )
        logging.info(
            f"end: set_address_line(line_number={line_number}, address_line={address_line})"
        )

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
        # Filter out empty or None values and join with ', '
        return ", ".join([part for part in address_parts if part])

    def get_address_line1(self) -> str:
        """
        Returns the first address line.
        """
        return self.address_line1

    def set_address_line1(self, address_line1: str) -> None:
        """
        Sets the first address line.
        """
        self.address_line1 = address_line1

    def get_address_line2(self) -> str:
        """
        Returns the second address line.
        """
        return self.address_line2

    def set_address_line2(self, address_line2: str) -> None:
        """
        Sets the second address line.
        """
        self.address_line2 = address_line2

    def get_address_line3(self) -> str:
        """
        Returns the third address line.
        """
        return self.address_line3

    def set_address_line3(self, address_line3: str) -> None:
        """
        Sets the thrid address line.
        """
        self.address_line3 = address_line3

    def get_address_line4(self) -> str:
        """
        Returns the fourth address line.
        """
        return self.address_line4

    def set_address_line4(self, address_line4: str) -> None:
        """
        Sets the fourth address line.
        """
        self.address_line4 = address_line4

    def get_address_line5(self) -> str:
        """
        Returns the fifth address line.
        """
        return self.address_line5

    def set_address_line5(self, address_line5: str) -> None:
        """
        Sets the fifth address line.
        """
        self.address_line5 = address_line5

    def get_post_code(self) -> str:
        """
        Returns the postcodde.
        """
        return self.post_code

    def set_post_code(self, post_code: str) -> None:
        """
        Sets the postcode.
        """
        self.post_code = post_code
