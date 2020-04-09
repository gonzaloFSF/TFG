from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from SimuladorApp.views import index, display_simulador, display_traza, display_download_file

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/?$', index, name="home_page"),
    url(r'^Simulador/?$', display_simulador, name="Simulador"),
    url(r'^Traza/?$', display_traza, name="Traza"),
    url(r'^Download_Traza/?$', display_download_file, name="Download_Traza"),
    url('', index, name="home_page")
]

