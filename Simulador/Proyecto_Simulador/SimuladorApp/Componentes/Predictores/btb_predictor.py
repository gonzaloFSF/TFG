
from SimuladorApp.Componentes.Bufferes.btb_buffer import BTB_BUFFER
from SimuladorApp.flags import FLAGS
import random


class BTB_PREDICTOR():
	
	pred_buffer = BTB_BUFFER()
	is_lru = 0
	insert_jump = None
	remove_entrie = None
	set_success_prediction = None
	set_failure_prediction = None
	remplace_entrie = None

	def __init__(self,args):

		ret_functions = {}
		functions = None

		self.pred_buffer = BTB_BUFFER(args)
		is_lru = args["is_lru"]
		self.get_configurable_functions(is_lru,ret_functions)
		functions = ret_functions["value"]
		self.insert_jump = functions['insert_jump']
		self.remove_entrie = functions['remove_entrie']
		self.set_success_prediction = functions['set_success_prediction']
		self.set_failure_prediction = functions['set_failure_prediction']
		self.remplace_entrie = functions['remplace_entrie']


	def get_jump_prediction(self,address_src,ret):

		retval = 0
		num_bits = self.pred_buffer.num_pred_bits
		ret_entrie = {}
		entrie = None
		prediction = None
		address_dts = None

		retval = self.get_data_entrie(address_src,ret_entrie)

		if(retval):
			return retval
		
		entrie = ret_entrie['value']
		address_dts = entrie['address_dts']
		bits_pred = entrie['bits']
		prediction = ( (bits_pred+1) > (2**(num_bits-1)) )
		ret['value'] = {
			'address_dts' : address_dts,
			'prediction' : prediction
		}

		return retval
		


	def get_bits_predictor(self,address_src,ret):

		retval = 0

		retval |= self.pred_buffer.get_bits_predictor(address_src,ret)

		return retval


	def get_data_entrie(self,address,ret):
	
		retval = 0

		retval |= self.pred_buffer.get_data_entrie(address,ret)

		return retval	   

	def insert_jump_ale(self,jump):
		
		retval = 0

		retval |= self.pred_buffer.insert_jump(jump)

		return retval

	def remove_entrie_ale(self,address,ret):
	
		retval = 0

		retval |= self.pred_buffer.remove_entrie(address,ret)

		return retval

	def set_success_prediction_ale(self,address,ret):

		retval = 0

		retval |= self.pred_buffer.increment_bits_predictor(address,ret)

		return retval

	def set_failure_prediction_ale(self,address,ret):
	
		retval = 0

		retval |= self.pred_buffer.decrement_bits_predictor(address,ret)

		return retval

	def remplace_entrie_ale(self,jump,ret):

		retval = 0
		len_branch_buffer = -1
		index = -1
		ret_len_branch_buffer = {}
		ret_address_remove = {}
		address_remove = None


		retval |= self.pred_buffer.get_size_branch_buffer(ret_len_branch_buffer)
		len_branch_buffer = ret_len_branch_buffer["value"]
		index = random.randint(0,len_branch_buffer - 1)
		retval |= self.pred_buffer.get_address_by_index(index,ret_address_remove)
		address_remove = ret_address_remove["value"]
		retval |= self.pred_buffer.remove_entrie(address_remove,ret)
		retval |= self.pred_buffer.insert_jump(jump) 

		return retval

	def insert_jump_lru(self,jump):

		retval = 0
		address_src = jump["address_src"]

		retval |= self.insert_jump_ale(jump)

		if not FLAGS.IS_BUFFER_LIMIT(retval):

			if FLAGS.IS_ENTRIE_EXIST(retval):

				self.pred_buffer.remove_entrie_lru_branch_stack(address_src)

			self.pred_buffer.insert_jump_lru_branch_stack(address_src)

		return retval

	def remove_entrie_lru(self,address,ret):
	
		retval = 0

		retval |= self.pred_buffer.remove_entrie(address,ret)

		if not FLAGS.IS_NOT_ADDRESS_REGISTER(retval):

			self.pred_buffer.remove_entrie(address,ret)

		return retval

	def set_success_prediction_lru(self,address,ret):

		retval = 0

		retval |= self.set_success_prediction_ale(address,ret)

		if not FLAGS.IS_NOT_ADDRESS_REGISTER(retval):

			self.pred_buffer.remove_entrie_lru_branch_stack(address)
			self.pred_buffer.insert_jump_lru_branch_stack(address)

		return retval


	def set_failure_prediction_lru(self,address,ret):
		
		retval = 0

		retval |= self.set_failure_prediction_ale(address,ret)

		if not FLAGS.IS_NOT_ADDRESS_REGISTER(retval):

			self.pred_buffer.remove_entrie_lru_branch_stack(address)
			self.pred_buffer.insert_jump_lru_branch_stack(address)

		return retval

	def remplace_entrie_lru(self,jump,ret):
		
		retval = 0
		ret_address_remove = {}
		address_remove = None
		address_insert = None
		num_free_entries = None
		ret_num_free_entries = {}

		self.pred_buffer.get_num_free_entries(ret_num_free_entries)
		num_free_entries = ret_num_free_entries["value"]

		if num_free_entries:
			return FLAGS.GET_ERROR_REMPLACE()	

		self.pred_buffer.get_entrie_by_index_lru_branch_stack(0,ret_address_remove)
		address_remove = ret_address_remove["value"]
		address_insert = jump["address_src"]
		retval |= self.pred_buffer.insert_jump(jump)
		
		if FLAGS.IS_ENTRIE_EXIST(retval) :
			
			self.pred_buffer.remove_entrie_lru_branch_stack(address_insert)

		else :
			
			self.pred_buffer.remove_entrie_lru_branch_stack(address_remove)
			self.pred_buffer.remove_entrie(address_remove,ret)
			self.pred_buffer.insert_jump(jump)

		self.pred_buffer.insert_jump_lru_branch_stack(address_insert)

		return retval


	
	def get_configurable_functions(self,is_lru,ret):

		retval = 0

		functions = [
			{
				'insert_jump' : self.insert_jump_ale,
				'remove_entrie' : self.remove_entrie_ale,
				'set_success_prediction' : self.set_success_prediction_ale,
				'set_failure_prediction' : self.set_failure_prediction_ale,
				'remplace_entrie' : self.remplace_entrie_ale

			},
			{
				'insert_jump' : self.insert_jump_lru,
				'remove_entrie' : self.remove_entrie_lru,
				'set_success_prediction' : self.set_success_prediction_lru,
				'set_failure_prediction' : self.set_failure_prediction_lru,
				'remplace_entrie' : self.remplace_entrie_lru
			}
		]
		
		ret["value"] = functions[is_lru]

		return retval



	
	