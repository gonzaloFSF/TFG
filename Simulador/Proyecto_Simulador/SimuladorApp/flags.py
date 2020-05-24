

from enum import Enum



class FLAGS(Enum):
    



    # Get flag


    @staticmethod
    def GET_BUFFER_LIMIT():
	    
        return (1 << 0)

    @staticmethod
    def GET_NOT_ADDRESS_REGISTER():

        return (1 << 1)

    @staticmethod
    def GET_COUNTER_SATURED():

        return (1 << 2)

    @staticmethod
    def GET_ENTRIE_EXIST():

        return (1 << 3)

    @staticmethod
    def GET_NOT_ADDRESS_REGISTER_LRU():

        return (1 << 4)

    @staticmethod
    def GET_ENTRIE_EXIST_LRU():

        return (1 << 5)

    @staticmethod
    def GET_ERROR_REMPLACE():

        return (1 << 6)

    @staticmethod
    def GET_END_TRACE():
	    
        return (1 << 7)

    @staticmethod
    def GET_SESSION_NOT_INIT():
	    
        return (1 << 8)


    @staticmethod
    def GET_NEW_ENTRIE_HISTORY_BUFFER():
	    
        return (1 << 9)


    # Find flag

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

    @staticmethod
    def IS_NOT_ADDRESS_REGISTER_LRU(retval):

        return retval & (1 << 4)

    @staticmethod
    def IS_ENTRIE_EXIST_LRU(retval):

        return retval & (1 << 5)

    @staticmethod
    def IS_ERROR_REMPLACE(retval):

        return retval & (1 << 6)

    @staticmethod
    def IS_END_TRACE(retval):

        return retval & (1 << 7)

    @staticmethod
    def IS_SESSION_NOT_INIT(retval):

        return retval & (1 << 8)


    @staticmethod
    def IS_NEW_ENTRIE_HISTORY_BUFFER(retval):
	    
        return retval & (1 << 9)





