from SimuladorApp.flags import FLAGS




class BITS_BUFFER_HISTORY():


    history_index = None
    bits_buffer = None
    counter = 0


    def __init__(self,history_index_len):

        self.bits_buffer = {}
        self.history_index = ['0']*history_index_len


    def handler_case(self,case):

        retval = 0

        if case == 1:

            self.history_index[self.counter] = '1'
            self.counter = (self.counter + 1) % len(self.history_index)
        
        elif case == 2:

            self.history_index[self.counter] = '0'
            self.counter = (self.counter + 1) % len(self.history_index)


        return retval


    def get_bits(self,case,ret):

        retval = 0
        index = "".join(self.history_index)


        try:

            ret['value'] = self.bits_buffer[index]

        except:

            retval |= FLAGS.GET_NEW_ENTRIE_HISTORY_BUFFER()
            self.bits_buffer[index] = {'bits' : 0}
            ret['value'] = self.bits_buffer[index]


        self.handler_case(case)


        return retval