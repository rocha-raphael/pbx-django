from django.contrib import admin
from django.urls import path
from . import views
from .paginas.home.home import *
from .paginas.pbx.pbx import *
from .paginas.adm.adm import *
from .paginas.globals.globals import *
from .paginas.painel.painel import *
from .paginas.relatorios.relatorios import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login', views.login, name='login'),
    path('', homeview, name='home'),
    path('pbx', pbxview, name='pbx'),
    path('ramais', ramaisview, name='ramais'),
    path('fila', filaview, name='fila'),
    path('grupos', gruposview, name='grupos'),
    path('teste', teste, name='teste'),
    #path('del_ramal', ramaisview, name='del_ramal'),
    #path('del_fila', filaview, name='del_fila'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
