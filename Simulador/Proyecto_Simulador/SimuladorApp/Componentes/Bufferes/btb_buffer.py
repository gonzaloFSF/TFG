
from SimuladorApp.flags import FLAGS

class BTB_BUFFER():

	branch_buffer = {}
	size_buffer = 0
	num_pred_bits = 0
	lru_branch_stack = []
	current_num_entries = 0
	init_bits_value = 0


	def __init__(self,*arguments):
		
		self.branch_buffer = {}
		self.size_buffer = 0
		self.num_pred_bits = 0
		self.lru_branch_stack = []
		self.current_num_entries = 0
		self.init_bits_value = 0

		if(len(arguments)):
			args = arguments[0]
			self.size_buffer = int(args["size_buffer"])
			self.num_pred_bits = int(args["num_pred_bits"])
			self.init_bits_value = int(args["init_bits_value"])

	

	def get_data_entrie(self,address,ret):

		retval = 0

		try :
			
			ret['value'] = self.branch_buffer[address]

		except KeyError:

			retval = FLAGS.GET_NOT_ADDRESS_REGISTER()

		return retval


	def get_address_by_index(self,index,ret):
	
		retval = 0

		ret['value'] = list(self.branch_buffer.keys())[index]

		return retval

	def get_size_branch_buffer(self,ret):
		
		retval = 0

		ret['value'] = len(self.branch_buffer.keys())

		return retval

	def get_num_free_entries(self,ret):

		retval = 0

		ret["value"] = self.size_buffer - self.current_num_entries

		return retval

	def insert_jump(self,jump):

		retval = 0
		address_src = jump["address_src"] 
		address_dts = jump["address_dts"] 
		entrie_exist = (address_src in list(self.branch_buffer.keys()))
		
		if(not entrie_exist and self.current_num_entries == self.size_buffer):

			retval |= FLAGS.GET_BUFFER_LIMIT()

		else:
			
			if not entrie_exist :

				self.current_num_entries += 1
				
			else:

				retval |= FLAGS.GET_ENTRIE_EXIST()
			
			data = {
				'address_src':address_src,
				'address_dts':address_dts,
				'bits' : self.init_bits_value
				}

			self.branch_buffer[address_src] = data

		return retval


	def remove_entrie(self,address,ret):

		retval = 0

		try :
			
			ret['value'] = self.branch_buffer.pop(address)
			self.current_num_entries -= 1

		except KeyError:

			retval = FLAGS.GET_NOT_ADDRESS_REGISTER()

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
		else:
			retval = FLAGS.GET_COUNTER_SATURED()

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
		else:
			retval = FLAGS.GET_COUNTER_SATURED()

		return retval






	def get_lru_branch_stack(self,ret):

		retval = 0

		ret["value"] = self.lru_branch_stack

		return retval

	
	def set_lru_branch_stack(self,new_lru_branch_stack):
		
		retval = 0

		self.lru_branch_stack = new_lru_branch_stack

		return retval


	def remove_entrie_lru_branch_stack(self,address):
		
		retval = 0

		try :
		
			self.lru_branch_stack.remove(address)
		
		except ValueError:

			retval |= FLAGS.GET_NOT_ADDRESS_REGISTER_LRU()
		
		return retval



	def insert_jump_lru_branch_stack(self,address):
		
		retval = 0
		
		if address in self.lru_branch_stack:
			
			retval |= FLAGS.GET_ENTRIE_EXIST_LRU()

		self.lru_branch_stack.append(address)
		
		return retval


	def get_entrie_by_index_lru_branch_stack(self,index,ret):

		retval = 0

		ret["value"] = self.lru_branch_stack[index]

		return retval


	def get_size_lru_branch_stack(self,ret):
	
		retval = 0

		ret["value"] = len(self.lru_branch_stack)

		return retval

		







	

	


