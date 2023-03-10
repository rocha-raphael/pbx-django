from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth import login as djandoLogin
from django.contrib.auth import logout as djandoLogout
from django.contrib.auth import authenticate
from .paginas.home.home import homeview




# Create your views here.

def login(request):
    if request.user.is_authenticated:
        pass #aqui estará logado, mandar para home
    else:
        if request.method == 'GET':
            return render(request, 'login.html')
        else:
           usuario = request.POST.get('usuario')
           senha = request.POST.get('senha')
           user = authenticate(username=usuario, password=senha)
           if user:
               djandoLogin(request, user)
               return redirect(homeview)
           else:
               return HttpResponse("login ou senha inválidos")
