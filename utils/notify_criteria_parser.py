import re

def parse_notify_criteria(criteria: str) -> dict:
    """
    Parses criteria strings like 'S1 - new' or 'S1 (S1w) - sending' into parts.
    """
    criteria = criteria.strip()
    if criteria.lower() == "none":
        return {"status": "none"}

    pattern = r"^(?P<type>[^\s(]+)(?:\s+\((?P<code>[^)]+)\))?\s*-\s*(?P<status>\w+)$"
    match = re.match(pattern, criteria, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid Notify criteria format: '{criteria}'")

    return {
        "type": match.group("type"),
        "code": match.group("code"),
        "status": match.group("status").lower(),
    }
