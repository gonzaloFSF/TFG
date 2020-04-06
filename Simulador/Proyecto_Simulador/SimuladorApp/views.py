from django.shortcuts import render
from SimuladorApp.forms import *
from SimuladorApp.models import Simulador
from SimuladorApp.flags import FLAGS

import os


def get_traza_files(home_dir):

	list_trazas = ["{}/{}".format(home_dir,file_traza) for file_traza in os.listdir(home_dir)]
	list_trazas = list(filter(lambda x: x[-4:] == '.out',list_trazas))
	res = {}

	for path_name in list_trazas:
		
		file_name = os.path.split(path_name)[-1]
		res[file_name] = {
		'Nombre' : file_name, 
		'Tamaño' : os.stat(path_name).st_size
		}

	return res


def create_traza(file_path,home_dir):
	

	list_trazas = []
	out_file = file_path.split('.')[0]+".o"
	out_traza = file_path.split('.')[0]+".out"
	
	os.system("gcc {} -o {}".format(file_path,out_file))
	os.system("FILE_PATH_TRAZA={} pin -t ../../Traza/pin/source/tools/dreamlandcoder/obj-intel64/global_trace.so -- {}".format(out_traza,out_file))
	
	os.system("rm {} {}".format(file_path,out_file))

	return list_trazas


def get_session(session):

	if not session.session_key:
		session.create()
	
	return session.session_key



def init_session(session):
	
	retval = 0
	session_id = get_session(session)
	
	home_path = "/tmp/tfg_sim/{}".format(session_id)
	os.makedirs(home_path,exist_ok=True)
	session['home_dir'] = home_path

	return retval

def test_session(session):
	
	retval = 0

	try:
	
		session["home_dir"]
	
	except:
		
		retval |= FLAGS.GET_SESSION_NOT_INIT()
	
	return retval
		

def handler_session_init(request):

	retval = 0
	
	retval |= test_session(request.session)

	if FLAGS.IS_SESSION_NOT_INIT(retval):

		init_session(request.session)


def handle_uploaded_file(request,file_form,home_dir):

	name_file = file_form.data['title']
	file = request.FILES['file']
	
	path_file = "{}/{}.c".format(home_dir,name_file)

	with open(path_file, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

	return path_file

def run_simulator(simulador):
	
	retval = 0
	ret_jump = {}
	counter = 0

	while(True):

		retval |= simulador.next_step_jump(ret_jump)
				
		if(FLAGS.IS_END_TRACE(retval)):
			break

		#print(counter)
		counter += 1

	return simulador

def handler_post_simulador_resultados(request,size,file_path,ret):

	retval = 0
	a = BTBForm(request.POST)

	form_copy = a.data.copy()
	form_copy['filename'] = file_path
	simulador = Simulador(form_copy)
	ret['value'] = {"resultado_{}".format(str(size+1)):run_simulator(simulador).json_fiels()}

	return retval



def handler_post_new_traza(file_form):
	pass



def index(request):

	return render(request, 'generic/index.html')

def display_simulador(request):

	handler_session_init(request)
	predictores_forms = {
		"pred_btb":BTBForm()
	}
	home_dir = request.session['home_dir']
	ret_lista_resultados = {}
	lista_resultados = request.session.get('resultados',{})
	lista_trazas = []
	listas = {}
	file_path = None
	print(request.POST)
	
	if request.POST:

		file_path = "{}/{}".format(home_dir,request.POST['code_row'])
		print(file_path)
		handler_post_simulador_resultados(request,len(lista_resultados.keys()),file_path,ret_lista_resultados)
		lista_resultados.update(ret_lista_resultados['value'])
	
	request.session['resultados'] = lista_resultados
	listas["Trazas"] = get_traza_files(home_dir)
	listas["Resultados"] = lista_resultados
	print(listas)

	return render(request, 'generic/simulador.html',{
		'predictores':["Predictor BTB"],
		'predictores_forms':predictores_forms,
		'listas' : listas
		})


def display_traza(request):

	handler_session_init(request)
	home_dir = request.session['home_dir']
	listas = {}
	
	if request.POST:

		file_form = UploadFileForm(request.POST)
		file_path = handle_uploaded_file(request,file_form,home_dir)
		list_trazas = create_traza(file_path,home_dir)

	listas["Trazas"] = get_traza_files(home_dir)
	form = UploadFileForm()

	return render(request, 'generic/traza.html',{
		'form':form,
		'listas' : listas
		})



