class Organisation:
    """
    Class representing an organisation with id, name, and code.
    """

    def __init__(self, new_id: int, new_name: str, new_code: str):
        self.id = new_id
        self.name = new_name
        self.code = new_code

    def get_name(self) -> str:
        """Returns the organisation name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Sets the organisation name"""
        self.name = name

    def get_id(self) -> int:
        """Returns the organisation id"""
        return self.id

    def set_id(self, id_: int) -> None:
        """Sets the organisation id"""
        self.id = id_

    def get_code(self) -> str:
        """Returns the organisation code"""
        return self.code

    def set_code(self, code: str) -> None:
        """Sets the organisation code"""
        self.code = code
