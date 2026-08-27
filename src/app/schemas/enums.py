from enum import Enum


class MerchantStatus(str, Enum):
    NORMAL = "normal"
    DISABLED = "disabled"
    CLOSED = "closed"


class AdminStatus(str, Enum):
    NORMAL = "normal"
    LOCKED = "locked"
