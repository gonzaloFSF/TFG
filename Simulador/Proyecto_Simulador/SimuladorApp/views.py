from django.shortcuts import render




def index(request):
    try:
        print(request.session['test'])
    except:
        print('pepe')
        pass
    request.session['test'] = 'prueba'
    return render(request, 'generic/index.html')


def display_simulador(request):
    pass

def display_traza(request):
    pass



