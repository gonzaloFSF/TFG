
from Simulador.Proyecto_Simulador.SimuladorApp.Componentes.Bufferes.btb_buffer import BTB_BUFFER


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

    def insert_entrie(self,entrie):
        
        retval = 0

        retval = self.btb_buffer.insert_entrie(entrie)

        if(self.lru):
            self.insert_entrie_lru(entrie["address"])

        return retval

    def remove_entrie(self,address,ret):
        
        retval = 0

        retval = self.btb_buffer.remove_entrie(address,ret)

        return retval


    def set_success_prediction(self,address,ret):

        retval = 0

        retval = self.btb_buffer.increment_bits_predictor(address,ret)

        return retval


    def set_failure_prediction(self,address,ret):
    
        retval = 0

        retval = self.btb_buffer.decrement_bits_predictor(address,ret)

        return retval
    
    
    def insert_entrie_lru(self,address):
        pass

    def lru_remplazar_entrie(self,entrie):
        pass

    def ale_remplazar_entrie(self,entrie):
        pass

    
    