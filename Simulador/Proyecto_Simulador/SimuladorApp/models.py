from django.db import models
from SimuladorApp.Componentes.Predictores.btb_predictor import BTB_PREDICTOR
from SimuladorApp.Componentes.Bufferes.btb_buffer import BTB_BUFFER
from SimuladorApp.flags import FLAGS
import pandas as pd


# sudo docker build -t gonzalofsf/tfg-simulador:test .
# docker container run --publish  222:22 --publish 8080:8080 --detach --name prueba gonzalofsf/tfg-simulador:test

class Simulador():
	
	predictor = None
	traza_file = None
	traza_string = None
	traza_list = None
	fails_prediction = 0
	success_prediction = 0
	remplace_jump = 0
	jump_counter = 0
		
	def __init__(self,config):

		
		ret_predictor = {}

		self.jump_counter = 0
		self.get_predictor(config,ret_predictor)
		self.predictor = ret_predictor['value']
		self.traza_list = list(pd.read_csv(config["filename"]).values)

	def __str__(self):

		return str({
			'fails_prediction' : self.fails_prediction,
			'success_prediction' : self.success_prediction,
			'remplace_jump' : self.remplace_jump
		})


	def next_step_jump(self,ret):

		retval = 0
		ret_jump = {}
		ret_prediction_dict = {}
		prediction_dict = None
		jump = None

		retval |= self.get_new_jump(ret_jump)

		if not (FLAGS.IS_END_TRACE(retval)):

			jump = ret_jump['value']
			address_src = jump['address_src']

			retval |= self.predictor.get_jump_prediction(address_src,ret_prediction_dict)

			if retval :

				if(FLAGS.IS_NOT_ADDRESS_REGISTER(retval)):

					retval |= self.predictor.insert_jump(jump)

				if(FLAGS.IS_BUFFER_LIMIT(retval)):

					retval |= self.predictor.remplace_entrie(jump,ret_jump)
					self.remplace_jump += 1
				
				self.predictor.get_jump_prediction(address_src,ret_prediction_dict)


			prediction_dict = ret_prediction_dict['value']

			if(str(jump['address_dts']) == prediction_dict['address_dts'] and  str(jump['was_jump']) == prediction_dict['prediction']):
			
				self.success_prediction += 1
			
			else:
			
				self.fails_prediction += 1

			if str(jump['was_jump']) == '1':
			
				self.predictor.set_success_jump(address_src,{})

			else:

				self.predictor.set_failure_jump(address_src,{})


			ret['value'] = [
						jump['address_src'], 
						jump['address_dts'] , 
						prediction_dict['address_dts'] , 
						jump['was_jump'],prediction_dict['prediction']
			]
			self.jump_counter += 1

		return retval



	def get_new_jump(self,ret):

		retval = 0
		jump_dict = {}

		try:

			jump_dict['address_src'] = self.traza_list[self.jump_counter][0]
			jump_dict['address_dts'] = self.traza_list[self.jump_counter][1]
			jump_dict['was_jump'] = self.traza_list[self.jump_counter][2]
			ret['value'] = jump_dict

		except IndexError:

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


	




