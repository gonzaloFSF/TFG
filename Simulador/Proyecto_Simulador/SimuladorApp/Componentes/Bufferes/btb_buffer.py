
from Simulador.Proyecto_Simulador.SimuladorApp.flags import FLAGS

class BTB_BUFFER():

    branch_buffer = {}
    size_buffer = 0
    num_pred_bits = 0
    lru_branch_stack = []
    current_num_entries = 0



    def __init__(self,args):

        self.size_buffer = args["size_buffer"]
        self.num_pred_bits = args["num_pred_bits"]

    

    def get_data_entrie(self,address,ret):

        retval = 0

        try :
            
            ret['value'] = self.branch_buffer[address]

        except KeyError:

            retval = FLAGS.NOT_ADDRESS_REGISTER

        return retval


    def insert_entrie(self,entrie):

        retval = 0
        address = entrie["address"]
        entrie_exist = (address in self.branch_buffer.keys())
        


        if(not entrie_exist and self.current_num_entries == self.size_buffer):

            retval = FLAGS.BUFFER_LIMIT

        else:
            
            if not entrie_exist :
                self.current_num_entries += 1
            else:
                retval = FLAGS.ENTRIE_EXIST
            
            data = entrie["data"]

            self.branch_buffer[address] = data

        return retval


    def remove_entrie(self,address,ret):

        retval = 0

        try :
            
            ret['value'] = self.branch_buffer.pop(address)

        except KeyError:

            retval = FLAGS.NOT_ADDRESS_REGISTER

        return retval


    def remplace_entrie(self,address,entrie,ret):

        retval = 0

        retval = self.remove_entrie(address,ret)

        if(retval):
            return retval

        retval = self.insert_entrie(entrie)

        return retval

    
    def get_bits_predictor(self,address,ret):

        retval = 0
        ret_data = {}

        retval = self.get_data_entrie(address,ret_data)
        
        if(retval):
            return retval

        data = ret_data["value"]


        ret["value"] = data["bits"]


        return retval
    

    
    def increment_bits_predictor(self,address,ret):

        retval = 0
        data = None
        ret_data = {}
        bits = -1

        retval = self.get_data_entrie(address,ret_data)
        
        if(retval):
            return retval


        data = ret_data["value"]
        bits = data["bits"]
        ret["value"] = bits

        if(bits < (2 ** (self.num_pred_bits)) - 1):
            data["bits"] = bits + 1
            retval = self.insert_entrie({"address":address,"data":data})
        else:
            retval = FLAGS.COUNTER_SATURED

        return retval


    def decrement_bits_predictor(self,address,ret):
    
        retval = 0
        data = None
        ret_data = {}
        bits = -1

        retval = self.get_data_entrie(address,ret_data)
        
        if(retval):
            return retval


        data = ret_data["value"]
        bits = data["bits"]
        ret["value"] = bits

        if(bits > 0):
            data["bits"] = bits - 1
            retval = self.insert_entrie({"address":address,"data":data})
        else:
            retval = FLAGS.COUNTER_SATURED

        return retval






    def get_lru_branch_stack(self,ret):

        retval = 0

        ret["value"] = self.lru_branch_stack

        return retval


    def set_lru_branch_stack(self,new_lru_branch_stack):
        
        retval = 0

        self.lru_branch_stack = new_lru_branch_stack

        return retval



    

    


