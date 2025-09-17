from enum import Enum


class KitStatus(Enum):
    """
    Enum representing kit statuses.
    """

    NEW = "NEW"
    LOGGED = "LOGGED"
    POSTED = "POSTED"
    AUTHORISED = "AUTHORISED"
    BCSS_READY = "BCSS_READY"
    BCSS_PROCESSING = "BCSS_PROCESSING"
    BCSS_PROCESSED = "BCSS_PROCESSED"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
