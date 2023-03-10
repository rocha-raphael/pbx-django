from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from ..pbx.pbx import pbxview
from ...models import Sippeers
from django.db import connections

#Variaveis globais aqui
HomePage='home/home.html'
GET='GET'
POST='POST'


# Create your views here.
@login_required(login_url='login')
def homeview(request):
    if request.method == GET:
        return render(request, HomePage)
    if request.method == POST:
        if 'homeBotao' in request.POST:
            return redirect(homeview)
            #return redirect(home)
        if 'homePainel' in request.POST:

            return HttpResponse('CLICOU NO PAINEL')
            #return redirect(painel)
        if 'homePbx' in request.POST:
            #return HttpResponse('CLICOU NO Estatisticas')
            return redirect(pbxview)
        if 'homeEst' in request.POST:
            return HttpResponse('CLICOU NO Estatisticas')
        if 'homeAdm' in request.POST:


            return HttpResponse('CLICOU NO Estatisticas')
            #return redirect(adm)
        if 'homeGlobal' in request.POST:
            return HttpResponse('CLICOU NO Estatisticas')
            #return redirect(pbx)
        else:
            return HttpResponse('CLICOU NO Estatisticas')
            #return redirect(home)

