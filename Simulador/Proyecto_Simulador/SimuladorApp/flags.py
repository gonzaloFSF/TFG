

from enum import Enum



class FLAGS(Enum):
    BUFFER_LIMIT = (1 << 0)
    NOT_ADDRESS_REGISTER = (1 << 1)
    COUNTER_SATURED = (1 << 2)
    ENTRIE_EXIST = (1 << 3)

    @staticmethod
    def IS_BUFFER_LIMIT(retval):
        return retval & (1 << 0)

    @staticmethod
    def IS_NOT_ADDRESS_REGISTER(retval):
        return retval & (1 << 1)

    @staticmethod
    def IS_COUNTER_SATURED(retval):
        return retval & (1 << 2)

    @staticmethod
    def IS_ENTRIE_EXIST(retval):
        return retval & (1 << 3)

