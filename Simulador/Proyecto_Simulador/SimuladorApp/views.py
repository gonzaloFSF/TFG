from django.shortcuts import render, redirect
from SimuladorApp.forms import *
from SimuladorApp.models import Simulador
from SimuladorApp.flags import FLAGS
from SimuladorApp.Aux_Code.download_files import *
from subprocess import check_output
import magic
import pickle

import os


def costum_exceptions(code):

	exceptions = {

		'1' : "El titulo es necesario",
		'2' : "Formato de archivo incorrecto",
		'3' : "No ha sido seleccionada ninguna traza",
		'4' : "No se ha seleccionado si el tipo de remplazo es lru o aleatorio",
		'5' : "Tamaño del buffer debe definirse y debe ser positivo",
		'6' : "Numero de bits de predicion debe definirse y debe ser positivo",
		'7' : "El número de ciclos por fallo debe definirse y debe ser positivo",
		'8' : "El tamaño del registro de desplazamiento debe definirse y debe ser positivo"
	
	}

	print("code {}".format(code))

	return exceptions[code]

def get_pred_form(pred_tipe):
	
	dict_forms = {
		'Predictor BTB': BTBForm,
		'Predictor de 2 niveles de historia':BTB2LEVESForm
	}
	
	return dict_forms[pred_tipe]

def get_handler(form_case):

	dict_handlers = {

		'Trazas_delete' : handler_eliminar_traza,
		'Trazas_send' : handler_post_simulador_resultados,
		'Resultados de pred_btb_delete' : handler_eliminar_resultado,
		'Upload':handle_uploaded_file,
		'Trazas_step':handler_init_simulador_step_by_step

	}

	return dict_handlers[form_case]

def handler_eliminar_traza(request,*args):

	if not ("traza_code_row" in request.POST.keys()) :
		raise Exception('3')
	
	home_dir = request.session.get('home_dir')
	file_name = request.POST['traza_code_row']
	file_path = os.path.join(home_dir,file_name)

	os.remove(file_path)

def handler_eliminar_resultado(request,*args):

	lista_nombre = request.POST['pred_id']
	
	for resultado_id in request.POST.getlist('code_row'):

		if not (lista_nombre in resultado_id) :
			continue

		all_list_results = request.session.get("resultados")
		print(all_list_results)
		list_results = all_list_results[lista_nombre]
		del list_results[resultado_id]
		print(list_results)
		print(resultado_id)
		all_list_results[lista_nombre] = list_results
		request.session["resultados"] = all_list_results


def get_traza_files(home_dir):

	list_trazas = ["{}/{}".format(home_dir,file_traza) for file_traza in os.listdir(home_dir)]
	list_trazas = filter(lambda x: not ("data_ser" in x), list_trazas)
	res = {}

	for path_name in list_trazas:
		
		file_name = os.path.split(path_name)[-1]
		res[file_name] = {
		'Nombre' : file_name, 
		'Saltos' : wc(path_name)
		}

	return res

def wc(filename):
	return int(check_output(["wc", "-l", filename]).split()[0])

def create_traza(file_path,arguments):
	

	list_trazas = []
	out_traza = file_path.split('.')[0]+".out"
	
	os.system("chmod +x {}".format(file_path))
	os.system("FILE_PATH_TRAZA={} pin -t ../../Traza/pin/source/tools/dreamlandcoder/obj-intel64/global_trace.so -- {} {}".format(out_traza,file_path,arguments))
	os.system("rm {}".format(file_path))

	return list_trazas


def get_session(session):

	if not session.session_key:
		session.create()
	
	return session.session_key



def init_session(session):
	
	retval = 0
	session_id = get_session(session)
	
	home_path = "/tmp/tfg_sim/{}".format(session_id)
	print(home_path)
	os.makedirs(home_path,exist_ok=True)
	session['home_dir'] = home_path

	return retval

def test_session(session):
	
	retval = 0


	try:
	
		os.stat(session.get("home_dir"))
	
	except:
		
		retval |= FLAGS.GET_SESSION_NOT_INIT()
	
	return retval
		

def handler_session_init(request):

	retval = 0
	
	retval |= test_session(request.session)

	if FLAGS.IS_SESSION_NOT_INIT(retval):

		init_session(request.session)


def handle_uploaded_file(request):

	file_form = UploadFileForm(request.POST)
	home_dir = request.session.get('home_dir')
	
	if file_form.data['title'] == "" :

		raise Exception("1")

	parts = file_form.data['title'].split(" ")
	name_file = parts[0]
	arguments = " ".join(parts[1:]) if len(parts) > 1 else []
	file = request.FILES['file']
	
	path_file = "{}/{}.o".format(home_dir,name_file)	

	with open(path_file, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)


	print(str(magic.from_file(path_file)))

	if not ("ELF" in str(magic.from_file(path_file))):
	
		os.remove(path_file)
		raise Exception("2")


	create_traza(path_file,arguments)

def handler_simalador_step_by_step(simulador):
	
	retval = 0
	ret_jump = {}



	retval |= simulador.next_step_jump(ret_jump)
				
	if(FLAGS.IS_END_TRACE(retval)):
		pass


	return simulador

def update_data_ser(file_path_ser,simulador):

	data_ser = pickle.dumps(
				{
					'jump_counter':simulador.jump_counter,
					'filename':simulador.file_name_data,
					'predictor':simulador.predictor,
					'fails_prediction' : simulador.fails_prediction,
					'success_prediction' : simulador.success_prediction,
					'remplace_jump' : simulador.remplace_jump,
					'instrucciones_totales':simulador.instrucciones_totales,

				})

	open(file_path_ser,"wb").write(data_ser)

def handler_init_simulador_step_by_step(request):

	if not ("traza_code_row" in request.POST.keys()) :
		raise Exception('3')

	home_dir = request.session.get('home_dir')
	file_path = "{}/{}".format(home_dir,request.POST['traza_code_row'])
	file_path_ser = "{}/{}".format(home_dir,"data_ser") 
	pred_tipe = request.POST['pred_id']
	form_copy = get_pred_form(pred_tipe)(request.POST).data.copy()
	form_copy['filename'] = file_path
	simulador = Simulador(form_copy)
	update_data_ser(file_path_ser,simulador)


def step_by_step_option(option):
	options = {
		'0':lambda x:True,
		'1':FLAGS.IS_FAIL_PREDICTION,
		'2':FLAGS.IS_BUFFER_LIMIT,
		'3':FLAGS.IS_SUCCESS_PREDICTION,
		'4':lambda x:False
	}

	return options[str(option)]

def run_simulator(simulador,option):
	
	retval = 0
	ret_jump = {}
	counter = 0

	while(True):

		retval |= simulador.next_step_jump(ret_jump)
				
		if(FLAGS.IS_END_TRACE(retval) or step_by_step_option(option)(retval)):
			break

		counter += 1

	return simulador

def get_unic_name(lista_resultados,size,pred_tipe):

	name = 	"resultado_{}__{}".format(str(size+1),pred_tipe)
	max_res = 100000
	index = 1

	try:

		lista_resultados[name]

		while(index < max_res):

			name = 	"resultado_{}__{}".format(index,pred_tipe)
			lista_resultados[name]
			index += 1

	except KeyError:
		pass

	return name




def handler_post_simulador_resultados(request):

	retval = 0
	
	if not ("traza_code_row" in request.POST.keys()) :
		raise Exception('3')

	home_dir = request.session.get('home_dir')
	file_path = "{}/{}".format(home_dir,request.POST['traza_code_row'])
	pred_tipe = request.POST['pred_id']
	name_res_tab = pred_tipe
	lista_resultados_global = request.session.get('resultados',{})
	lista_resultados = None
	try:

		lista_resultados = lista_resultados_global[name_res_tab]
		print(lista_resultados)

	except KeyError:

		print("holaaaaaaaaaaaaaaaaaaaaaaaaaa")
		lista_resultados = {}

	
	size = len(lista_resultados.keys())
	form_copy = get_pred_form(pred_tipe)(request.POST).data.copy()
	form_copy['filename'] = file_path
	simulador = Simulador(form_copy)
	sim_res = {"Archivo" : os.path.split(file_path)[-1]}
	sim_res.update(run_simulator(simulador,4).json_fiels())
	lista_resultados.update({get_unic_name(lista_resultados,size,pred_tipe):sim_res})
	lista_resultados_global[name_res_tab] = lista_resultados
	request.session['resultados'] = lista_resultados_global

	return retval





def index(request):

	return render(request, 'generic/index.html')

def display_download_file(request):

	return download_file(request)

def display_simulador(request):

	

	handler_session_init(request)
	predictores_forms = {
		'Predictor BTB': BTBForm(),
		'Predictor de 2 niveles de historia':BTB2LEVESForm()
	}
	home_dir = request.session['home_dir']
	listas = {}
	trazas = {}
	form_case = None
	errors = None
	print(request.POST)

	try:
		if request.POST:

			form_case = request.POST['sendform']
			get_handler(form_case)(request)

	except Exception as e:

		errors = costum_exceptions(str(e))


	if form_case != "Trazas_step" or errors != None:

		trazas["Trazas"] = get_traza_files(home_dir)

		if 'resultados' in request.session.keys():
			
			listas.update(request.session['resultados'])


		return render(request, 'generic/simulador.html',{
			'predictores':["Predictor BTB","Predictor de 2 niveles de historia"],
			'predictores_forms':predictores_forms,
			'listas' : listas,
			'trazas':trazas,
			'errors':errors
			})
	
	else:

		return redirect("http://{}/{}".format(request.META['HTTP_HOST'],'Sim_Step_By_Step/'))


def display_traza(request):

	handler_session_init(request)
	home_dir = request.session['home_dir']
	listas = {}
	errors = None
	print(request.POST)

	if request.POST:

		try:

			form_case = request.POST['sendform']
			get_handler(form_case)(request)

		except Exception as e:
			
			errors = costum_exceptions(str(e))
			print(errors)
			
	listas["Trazas"] = get_traza_files(home_dir)
	form = UploadFileForm()

	return render(request, 'generic/traza.html',{
		'form':form,
		'listas' : listas,
		'errors' : errors
		})

#simulador = handler_simalador_step_by_step(simulador)

def get_simulator_current_state(request):

	home_dir = request.session['home_dir']
	file_path_ser = "{}/{}".format(home_dir,"data_ser") 
	simulador = None
	data_ser = None
	data_desser = None
	data_ser = open(file_path_ser,"rb").read()
	data_desser = pickle.loads(data_ser)
	simulador = Simulador(
				data_desser['jump_counter'],
				data_desser['predictor'],
				data_desser['filename'],
				data_desser['fails_prediction'],
				data_desser['success_prediction'],
				data_desser['remplace_jump'],
				data_desser['instrucciones_totales'],
			     )

	return simulador


def display_get_next_step(request,option):

	home_dir = request.session['home_dir']
	file_path_ser = "{}/{}".format(home_dir,"data_ser")
	simulador = None
	current_jump = {}

	simulador = get_simulator_current_state(request)
	simulador = run_simulator(simulador,option)
	simulador.get_new_jump(current_jump)


		
	
	update_data_ser(file_path_ser,simulador)

	return display_simulador_step_by_step(request)

def display_simulador_step_by_step(request):

	handler_session_init(request)
	current_jump = {}
	tables = {}
	simulador = None
	errors = None

	simulador = get_simulator_current_state(request)

	simulador.get_new_jump(current_jump)
	current_jump = {'current_jump':current_jump}
	tables['Resultados'] = {'resultados':simulador.json_fiels()}
	tables['Buffer'] = simulador.predictor.pred_buffer.format_to_display()


	
	return render(request, 'generic/sim_step_by_step.html',{
		'tables':tables,
		'current_jump':current_jump,
		'errors':errors
		})



