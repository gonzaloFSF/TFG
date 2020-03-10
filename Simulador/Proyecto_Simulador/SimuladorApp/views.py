from django.shortcuts import render
from SimuladorApp.forms import *





def index(request):

    return render(request, 'generic/index.html')

def display_simulador(request):
    
    predictores_forms = {
        "Predictor BTB":BTBForm()
    }

    return render(request, 'generic/simulador.html',{
        'predictores':["Predictor BTB"],
        'predictores_forms':predictores_forms
        })

def display_traza(request):
    
    pass



