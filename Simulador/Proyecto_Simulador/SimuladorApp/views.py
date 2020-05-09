from django.shortcuts import render
from SimuladorApp.forms import *
from SimuladorApp.models import Simulador
from SimuladorApp.flags import FLAGS
from SimuladorApp.Aux_Code.download_files import *
from subprocess import check_output
import magic


import os


def costum_exceptions(code):

	exceptions = {

		'1' : "El titulo es necesario",
		'2' : "Formato de archivo incorrecto",
		'3' : "No ha sido seleccionada ninguna traza",
	}

	print("code {}".format(code))

	return exceptions[code]

def get_pred_form(pred_tipe):
	
	dict_forms = {
		'pred_btb' : BTBForm
	}
	
	return dict_forms[pred_tipe]

def get_handler(form_case):

	dict_handlers = {

		'Trazas_delete' : handler_eliminar_traza,
		'Trazas_send' : handler_post_simulador_resultados,
		'Resultados de pred_btb_delete' : handler_eliminar_resultado,
		'Upload':handle_uploaded_file

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

	lista_nombre = request.POST['sendform'].split("_delete")[0]
	resultado_id = request.POST['code_row']
	all_list_results = request.session.get("resultados")
	list_results = all_list_results[lista_nombre]
	del list_results[resultado_id]
	print(list_results)
	print(resultado_id)
	all_list_results[lista_nombre] = list_results
	request.session["resultados"] = all_list_results

def get_traza_files(home_dir):

	list_trazas = ["{}/{}".format(home_dir,file_traza) for file_traza in os.listdir(home_dir)]
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
	
		session["home_dir"]
	
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


	print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	

	with open(path_file, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)


	print(str(magic.from_file(path_file)))

	if not ("ELF" in str(magic.from_file(path_file))):
	
		os.remove(path_file)
		raise Exception("2")


	create_traza(path_file,arguments)


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


def handler_post_simulador_resultados(request):

	retval = 0
	
	if not ("traza_code_row" in request.POST.keys()) :
		raise Exception('3')

	home_dir = request.session.get('home_dir')
	file_path = "{}/{}".format(home_dir,request.POST['traza_code_row'])
	pred_tipe = request.POST['predictor']
	name_res_tab = 'Resultados de {}'.format(pred_tipe)
	lista_resultados_global = request.session.get('resultados',{})
	lista_resultados = None
	try:

		lista_resultados = lista_resultados_global[name_res_tab]

	except KeyError:

		lista_resultados = {}

	
	size = len(lista_resultados.keys())
	form_copy = get_pred_form(pred_tipe)(request.POST).data.copy()
	print(form_copy)
	form_copy['filename'] = file_path
	simulador = Simulador(form_copy)
	sim_res = {"Archivo" : os.path.split(file_path)[-1]}
	sim_res.update(run_simulator(simulador).json_fiels())
	lista_resultados.update({"resultado_{}__{}".format(str(size+1),pred_tipe):sim_res})
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
		"pred_btb":BTBForm()
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

		errors = str(e)
		

	trazas["Trazas"] = get_traza_files(home_dir)

	if 'resultados' in request.session.keys():
		
		listas.update(request.session['resultados'])


	return render(request, 'generic/simulador.html',{
		'predictores':["Predictor BTB"],
		'predictores_forms':predictores_forms,
		'listas' : listas,
		'trazas':trazas,
		'errors':errors
		})


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
			print("pepeeeeeeeeeeeeeeeeeeeeeeeeee")
			
	listas["Trazas"] = get_traza_files(home_dir)
	form = UploadFileForm()

	return render(request, 'generic/traza.html',{
		'form':form,
		'listas' : listas,
		'errors' : errors
		})



