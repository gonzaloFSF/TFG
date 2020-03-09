from django.shortcuts import render




def index(request):
    request.session['test'] = 'prueba'
    return render(request, 'generic/index.html')


def display_simulador(request):
    pass

def display_traza(request):
    pass



# git add . && git commit -m "Prueba variable sesion" && git push