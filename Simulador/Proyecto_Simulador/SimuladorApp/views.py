from django.shortcuts import render
from SimuladorApp.forms import *
from SimuladorApp.models import Simulador
from SimuladorApp.flags import FLAGS






def index(request):

    return render(request, 'generic/index.html')

def display_simulador(request):

    predictores_forms = {
        "pred_btb":BTBForm()
    }
    listas = []
    lista_resultados = []
    res = []

    if request.POST:

        a = BTBForm(request.POST)
        form_copy = a.data.copy()
        form_copy['filename'] = '../../Traza/traza.out'
        simulador = Simulador(form_copy)
        res = [run_simulator(simulador).json_fiels()]

    res += request.session.get('resultados',[])
    request.session['resultados'] = res
    lista_resultados += res
    listas.append(lista_resultados)
    print(listas)

    return render(request, 'generic/simulador.html',{
        'predictores':["Predictor BTB"],
        'predictores_forms':predictores_forms,
        'listas' : listas
        })


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

def display_traza(request):
    
    pass



