from django.shortcuts import render




def index(request):
    print(username)
    return render(request, 'generic/index.html')
