from dataclasses import dataclass


@dataclass
class UserRoleType:
    org_code: str
    user_code: str
    role_id: int
