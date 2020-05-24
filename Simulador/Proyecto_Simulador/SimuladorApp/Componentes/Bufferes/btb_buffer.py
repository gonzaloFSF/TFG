
from SimuladorApp.flags import FLAGS
from SimuladorApp.Componentes.Bufferes.btb_2_nivel import BITS_BUFFER_HISTORY

class BTB_BUFFER():

	branch_buffer = {}
	size_buffer = 0
	num_pred_bits = 0
	lru_branch_stack = []
	current_num_entries = 0
	is_simple_buffer = 0
	history_index_len = 0
	buffer_history_index = {}


	def __init__(self,*arguments):
		
		self.branch_buffer = {}
		self.size_buffer = 0
		self.num_pred_bits = 0
		self.lru_branch_stack = []
		self.current_num_entries = 0
		self.buffer_history_index = {}

		if(len(arguments)):
			args = arguments[0]
			self.comprobar_parametros(args)
			self.size_buffer = int(args["size_buffer"])
			self.num_pred_bits = int(args["num_pred_bits"])
			self.is_simple_buffer = int(args["is_simple_buffer"])
			
			if not self.is_simple_buffer:

				self.history_index_len = int(args["history_index_len"])



	def comprobar_parametros(self,args):


		if not ('size_buffer' in args.keys() and len(args["size_buffer"]) > 0 and int(args["size_buffer"]) > 0):
			
			raise Exception('5')

		if not ('num_pred_bits' in args.keys() and len(args["num_pred_bits"]) > 0 and int(args["num_pred_bits"]) > 0):
			
			raise Exception('6')

		if not args["is_simple_buffer"] and not ('history_index_len' in args.keys() and len(args["history_index_len"]) > 0 and int(args["history_index_len"]) > 0):

			raise Exception('8')

	def format_values(self,ele):

		num_zeros = 0
		zeros_add = ""
		bits = ""
		ret_bits = {}

		bits = ele['bits']

		if not (self.is_simple_buffer):

			self.get_bits_predictor(ele['address_src'],ret_bits)
			bits = ret_bits['value']
			ele['Historial de Saltos'] = ("".join(ele['bits'].history_index))[::-1]
			ele['Contador Desplazamiento'] = ele['bits'].counter

		bits = str(bin(bits))[2:]
		num_zeros = self.num_pred_bits - (len(bits))
		zeros_add = "0"*num_zeros

		ele['bits'] = zeros_add+bits

	def format_to_display(self):

		btb_buffer_cp_dict = {}
		btb_buffer_cp_list = [value.copy() for key,value in self.branch_buffer.items()]
		

		for ele in btb_buffer_cp_list:

			ele.pop('address_dts')
			self.format_values(ele)
			key = list(ele.values())[1]
			btb_buffer_cp_dict[key] = ele

		print(btb_buffer_cp_dict)

		return btb_buffer_cp_dict

	def to_json(self):

		return {
			
			'branch_buffer':self.format_to_display(),
			'size_buffer':self.size_buffer,
			'num_pred_bits':self.num_pred_bits,
			'lru_branch_stack':self.lru_branch_stack,
			'current_num_entries':self.current_num_entries,
		}



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
		instruccion = jump["instruccion"] 
		address_src = jump["address_src"] 
		address_dts = jump["address_dts"] 
		entrie_exist = (address_src in list(self.branch_buffer.keys()))
		ret_bits = {}
		bits = -1
		
		if(not entrie_exist and self.current_num_entries == self.size_buffer):

			retval |= FLAGS.GET_BUFFER_LIMIT()

		else:
			
			if not entrie_exist :

				self.current_num_entries += 1
				
			else:

				retval |= FLAGS.GET_ENTRIE_EXIST()

			retval |= self.get_init_bits(address_src,ret_bits)
			bits = ret_bits['value']
			
			data = {
				'instruccion':instruccion,
				'address_src':address_src,
				'address_dts':address_dts,
				'bits' : bits
				}

			self.branch_buffer[address_src] = data

		return retval

	def get_init_bits(self,address,ret):

		retval = 0
		address_part = None
		
		address_part = address[4:]

		if self.is_simple_buffer:

			ret['value'] = 0

		else:

			try :

				ret['value'] = self.buffer_history_index[address_part]

			except KeyError:

				self.buffer_history_index[address_part] = BITS_BUFFER_HISTORY(self.history_index_len)
				ret['value'] = self.buffer_history_index[address_part]

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

		retval = self.extract_bits(address,0,ret_data)
		data = ret_data["value"]
		ret["value"] = data["bits"]


		return retval
	

	
	def increment_bits_predictor(self,address,ret):

		retval = 0
		data = None
		ret_data = {}
		bits = -1

		retval = self.extract_bits(address,1,ret_data)
		
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

		retval = self.extract_bits(address,2,ret_data)
		
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


	def set_dts_address(self,address_src,address_dts):
		
		retval = 0

		self.branch_buffer[address_src]["address_dts"] = address_dts

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


	def extract_bits(self,address,case,ret):
		
		retval = 0
		ret_bits = {}
		ret_entrie = {}
		entrie = None

		retval |= self.get_data_entrie(address,ret_entrie)
		entrie = ret_entrie['value']

		if self.is_simple_buffer:

			ret['value'] = entrie

		else:

			retval |= entrie['bits'].get_bits(case,ret_bits)
			ret['value'] = ret_bits['value']


		return retval
		
		

		







	

	


