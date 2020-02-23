

from enum import Enum



class FLAGS(Enum):
    BUFFER_LIMIT = (1 << 0)
    NOT_ADDRESS_REGISTER = (1 << 1)
    COUNTER_SATURED = (1 << 2)