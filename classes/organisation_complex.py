from typing import Optional


class Organisation:
    """
    Class representing an organisation with id, name, and code.
    """

    def __init__(
        self,
        new_id: Optional[int] = None,
        new_name: Optional[str] = None,
        new_code: Optional[str] = None,
    ):
        self.id = new_id
        self.name = new_name
        self.code = new_code
