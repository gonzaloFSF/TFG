from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from SimuladorApp.views import index, display_simulador, display_traza, display_download_file, display_simulador_step_by_step, display_get_next_step

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^Home/?$', index, name="home_page"),
    url(r'^Simulador/?$', display_simulador, name="Simulador"),
    url(r'^Traza/?$', display_traza, name="Traza"),
    url(r'^Download_Traza/?$', display_download_file, name="Download_Traza"),
    url(r'^Sim_Step_By_Step/?$', display_simulador_step_by_step, name="Sim_Step_By_Step"),
    url(r'^Get_next_step/?$', display_get_next_step, name="get_next_step"),
    url('', index, name="home_page")
]

