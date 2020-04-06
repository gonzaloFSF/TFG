from django.test import TestCase
from SimuladorApp.models import Simulador
from SimuladorApp.flags import FLAGS



def btb_test():

	retval = 0
	file_prove = None
	ret_jump = {}
	jump = None
	counter = 0
	config = {
		'filename':'../../Traza/traza.out',
		'pred_id':'Predictor BTB',
		'is_lru':0,
		'size_buffer':8,
		'num_pred_bits':2,
		'init_bits_value':2
	}
	simulador = Simulador(config)

	print("#################################################\n\n")

	while(True):

		retval |= simulador.next_step_jump(ret_jump)
		
		if(FLAGS.IS_END_TRACE(retval)):
			break

		jump = ret_jump['value']
		
		
		if(True or "235" in jump[0]):
			print_all(simulador,jump)

		print(counter)
		counter += 1

	return simulador
		

def print_all(simulador,jump):
	
	print("Buffer : {}".format(simulador.predictor.pred_buffer.branch_buffer))
	print("Lru stack : {}".format(simulador.predictor.pred_buffer.lru_branch_stack))
	print("Simulador : {}".format(simulador))
	print("Jump : {}".format(jump))
	print("\n\n#################################################\n\n")
	
	if(input() == "10"):
		exit()
