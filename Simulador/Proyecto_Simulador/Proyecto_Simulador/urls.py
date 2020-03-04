from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from SimuladorApp.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/?$', index, name="home_page"),
    url('', index, name="home_page")
]

