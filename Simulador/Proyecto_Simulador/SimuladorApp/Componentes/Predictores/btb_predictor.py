
from Simulador.Proyecto_Simulador.SimuladorApp.Componentes.Bufferes.btb_buffer import BTB_BUFFER
from Simulador.Proyecto_Simulador.SimuladorApp.flags import FLAGS



class BTB_PREDICTOR():
    
    btb_buffer = BTB_BUFFER(None)
    remplazar_entrie = None
    is_lru = 0

    def __init__(self,args):

        self.btb_buffer = args["buffer"]
        is_lru = args["is_lru"]

    def get_data_entrie(self,address,ret):
        
        retval = 0

        retval = self.btb_buffer.get_data_entrie(address,ret)

        return retval       

    def insert_entrie_ale(self,entrie):
        
        retval = 0

        retval = self.btb_buffer.insert_entrie(entrie)

        return retval

    def remove_entrie_ale(self,address,ret):
        
        retval = 0

        retval = self.btb_buffer.remove_entrie(address,ret)

        return retval


    def set_success_prediction_ale(self,address,ret):

        retval = 0

        retval = self.btb_buffer.increment_bits_predictor(address,ret)

        return retval


    def set_failure_prediction_ale(self,address,ret):
    
        retval = 0

        retval = self.btb_buffer.decrement_bits_predictor(address,ret)

        return retval


     def ale_remplazar_entrie(self,entrie):
        pass



    def insert_entrie_lru(self,entrie):
        
        retval = 0
        ret_lru_stack = {}
        address = None
        lru_stack = None 

        retval = self.insert_entrie_ale(entrie)
        retval |= self.btb_buffer.get_lru_branch_stack(lru_stack)
        address = entrie["address"]
        lru_stack = ret_lru_stack["value"]

        if FLAGS.IS_ENTRIE_EXIST :
            lru_stack.remove(address)
        
        lru_stack.append(address)



        return retval

    def remove_entrie_lru(self,address,ret):
        
        retval = 0

        retval = self.btb_buffer.remove_entrie(address,ret)

        return retval


    def set_success_prediction_lru(self,address,ret):

        retval = 0

        retval = self.btb_buffer.increment_bits_predictor(address,ret)

        return retval


    def set_failure_prediction_lru(self,address,ret):
    
        retval = 0

        retval = self.btb_buffer.decrement_bits_predictor(address,ret)

        return retval

    def lru_remplazar_entrie(self,entrie):
        pass


    
    