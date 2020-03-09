from django.db import models
from Componentes.Predictores.btb_predictor import BTB_PREDICTOR
from Componentes.Bufferes.btb_buffer import BTB_BUFFER
from flags import FLAGS


# sudo docker build -t gonzalofsf/tfg-simulador:test .
# docker container run --publish  222:22 --publish 8080:8080 --detach --name prueba gonzalofsf/tfg-simulador:test

class Simulador():
    
    predictor = BTB_PREDICTOR()
    traza_file = None
    traza_string = None
    traza_list = None
    fails_prediction = 0
    success_prediction = 0
    remplace_jump = 0

    def __init__(self,config):
        
        ret_predictor = {}
        
        self.get_predictor(config,ret_predictor)
        self.predictor = ret_predictor['value']


    def next_step_jump(self):
        
        retval = 0
        ret_jump = {}
        ret_prediction_dict = {}
        prediction_dict = None
        jump = None
        was_jump = None

        retval |= self.get_new_jump(ret_jump)

        if not (FLAGS.IS_END_TRACE(retval)):

            jump = ret_jump['value']
            address_src = jump['address_src']

            retval |= self.predictor.get_jump_prediction(address_src,ret_prediction_dict)

            if(FLAGS.IS_NOT_ADDRESS_REGISTER(retval)):

                retval |= self.predictor.insert_jump(jump)

            if(FLAGS.IS_BUFFER_LIMIT(retval)):

                retval |= self.predictor.remplace_entrie(jump,ret_jump)
                self.remplace_jump += 1


            prediction_dict = ret_prediction_dict['value']

            if(
                jump['address_dts'] == prediction_dict['address_dts'] and
                jump['was_jump'] == prediction_dict['prediction']
            ):
                self.success_prediction += 1
            else:
                self.fails_prediction += 1


        return retval



    def get_new_jump(self,ret):

        retval = 0
        jump_dict = {}
        jump_split = None

        try:

            jump_split = self.traza_list.pop(0).split(',')
            jump_dict['address_src'] = jump_split[0]
            jump_dict['address_dts'] = jump_split[1]
            jump_dict['was_jump'] = jump_split[2]
            ret['value'] = jump_dict

        except IndexError as e:

            retval |= FLAGS.GET_END_TRACE()

        return retval



    def get_predictor(self,config,ret):

        retval = 0
        map_predicto = {
            '0':BTB_PREDICTOR
        }
        preditor_id = config['predictor_id']

        ret['value'] = map_predicto[preditor_id](config)

        return retval


	def get_prediction_jump(self,jump,ret):

		retval = 0
		address_src = jump['address_src']

		retval |= self.predictor.get_bits_predictor(address_src,ret)

		return retval


    




