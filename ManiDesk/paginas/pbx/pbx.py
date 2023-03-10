from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from ...servicos.querys_banco import *
#from ...models import UploadedFile
#from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

#Variaveis globais aqui
TabelaSipPeers='sippeers'
TabelaFilas='filas'
TabelaDids='dids'
TabelaGrupos='grupos'
TabelaGlobais='globais'

#Variavais de pagina
PopUpEditar='pbx/popup_editar.html'
RamaisPage='pbx/ramais/ramais.html'
GruposPage='pbx/grupos/grupos.html'
FilaPage='pbx/filas/filas.html'
AudioPage='pbx/audio/audio.html'
PbxPage='pbx/pbx.html'
GET='GET'
POST='POST'
contextos=['todas','local_celular', 'local_fixo_ddd']

#Busca gerais do banco
#todos os alias das filas na base de dados ipbx.filas

#todos os ID's das filas na base de dados ipbx.filas
IDFilas = listarUniColAll('id', 'filas','id')
#Busca os enum do banco com as estratégias
estrategias = tiposEnum('filas','strategy')
toques=[0,3,4,5]

listaAbas=[1,2,3,4,5]

@login_required(login_url='login')
def pbxview(request):
    if request.method == GET:
        return render(request, PbxPage)
    else:
        ramais = request.POST.get('ramais')
        fila = request.POST.get('fila')
        grupos = request.POST.get('grupos')
        tempo = request.POST.get('tempo')
        audio = request.POST.get('audio')
        #nome_da_fila=  #buscar o nome da fila no banco
        if ramais is not None:
            return redirect(ramaisview)
        if fila is not None:
            return redirect(filaview)
        if audio is not None:
            return redirect(teste)
        if grupos is not None:
            return redirect(gruposview)
        return redirect(pbxview)

@login_required(login_url='login')
def ramaisview(request):
    if request.method == GET:
        return render(request, RamaisPage)
    else:
        incluir = request.POST.get('incluir')
        criar = request.POST.get('create')
        ver = request.POST.get('read')
        popup_atualizar = request.POST.get('popup_atualizar')
        excluir_ramal = request.POST.get('excluir_ramal')
        fechar_editar = request.POST.get('fechar_editar')
        atualizacao = request.POST.get('atualizacao')
        existente=None
        ramal = None
        entendido = request.POST.get('entendido')

        if incluir is not None:
            ramais=listarUniColAll('name',TabelaSipPeers,'name')
            ramal = request.POST.get('ramal')
            if ramal in ramais:
                existente=True
            else:
                inclusao = [ramal]
                for i in ('nome','senha','contexto','grupo','grupo','tronco','grava'):
                    incluir = request.POST.get(i)
                    if i == 'grava':
                        if incluir is None:
                            incluir = 'no'
                    if incluir is None:
                        incluir=" "
                    if incluir == 'sim':
                        incluir = "yes"
                    inclusao.append(incluir)
                inclusao[4]=buscaExata('id',TabelaGrupos,'grupo',inclusao[4])
                inclusao[5]=buscaExata('id', TabelaGrupos, 'grupo', inclusao[5])
                colunas = ['name', 'fullname', 'secret', 'context', 'pickupgroup', 'callgroup', 'trunkname', 'gravar']
                incluirRamal(TabelaSipPeers,colunas,inclusao)

        #Atualizar os ramais
        if atualizacao is not None:
            ramalAtualizar = request.POST.get('ramalAtualizar')
            nomeNovo = request.POST.get('nomeAtualizar')
            senhaNova = request.POST.get('senhaAtualizar')
            contextoNovo = request.POST.get('contextoAtualizar')
            grupoNovo = request.POST.get('grupoAtualizar')
            troncoNovo = request.POST.get('troncoAtualizar')
            gravaNovo = request.POST.get('gravaAtualizar')
            if gravaNovo is None:
                gravaNovo='no'
            try:
                grupoNovo=buscaExata('id',TabelaGrupos,'grupo',grupoNovo)
            except Exception as e:
                print(e)
            listaAtual=(nomeNovo,senhaNova,contextoNovo,grupoNovo,grupoNovo,troncoNovo,gravaNovo)
            listaColunas=('fullname','secret','context','pickupgroup','callgroup','trunkname','gravar')
            AtualizarRamais(TabelaSipPeers,listaColunas,listaAtual,'name',ramalAtualizar)
            pass

        #EXCLUIR RAMAIS
        if excluir_ramal is not None:
            deletarBanco(TabelaSipPeers,'id',excluir_ramal)
            pass

        #CRIAR RAMAIS
        if any(i is not None for i in [criar,incluir,entendido]):
            create = True
            pagina = PagRamaisListas()
            return render(request, RamaisPage, {"create": create,'lista_de_ramais':pagina[0],
                    'lista_de_grupos':pagina[1],'lista_de_troncos':pagina[2], 'contextos':contextos, 'existente':existente, "ramal":ramal})

        #VER RAMAIS
        if any(i is not None for i in [ver,fechar_editar,atualizacao,excluir_ramal]):
        #if ver is not None or fechar_editar is not None or atualizacao is not None or excluir_ramal is not None:
            pagina = PagRamaisListas()
            read = True
            return render(request, RamaisPage, {"read": read,'lista_de_ramais':pagina[0],
                    'lista_de_grupos':pagina[1],'lista_de_troncos':pagina[2]})

        #POPUP DE EDICAO DOS RAMAIS
        if popup_atualizar is not None :
            pagina = PagRamaisListas()
            editar_ramal = listar_edicao(popup_atualizar)
            return render(request, RamaisPage, {"read": True, 'lista_de_ramais': pagina[0],'lista_de_grupos':pagina[1],
               'lista_de_troncos': pagina[2],'popup_atualizar':popup_atualizar, "editar_ramal":editar_ramal, 'contextos':contextos})

@login_required(login_url='login')
def filaview(request):
    if request.method == 'GET':
        idFila = 1
        nome_da_fila = buscaExata('alias', TabelaFilas, 'id', idFila)
        estrategia_atual = buscaExata('strategy', TabelaFilas, 'id', idFila)
        toque_atual = buscaExata('timeout', TabelaFilas, 'id', idFila)
        anuncio_atual = buscaExata('announce', TabelaFilas, 'id', idFila)
        lista_ramais = listarUniColAll('name',TabelaSipPeers, 'id')
        lista_filas_atual = listarLike('name',TabelaSipPeers,'fila',idFila)
        if toque_atual <= 15:
            toque_atual = 3
        if toque_atual >= 16 and toque_atual <= 24:
            toque_atual = 4
        if toque_atual >= 25:
            toque_atual = 5
        # ramais_atual = buscaExata('alias','filas','id',filaAlias[0])
        NomeFilas = listarUniColAll('alias', TabelaFilas, 'id')
        FilasGeral = zip(IDFilas, NomeFilas)
        return render(request, FilaPage, {'idFila': idFila, 'FilasGeral': FilasGeral, 'nome_da_fila': nome_da_fila,
                                          'estrategia_atual': estrategia_atual, 'toque_atual': toque_atual,
                                          'anuncio_atual': anuncio_atual,'lista_ramais':lista_ramais,'lista_filas_atual':lista_filas_atual,
                                          'estrategias': estrategias, 'toques': toques})
    else:
        filaAlias = request.POST.get('filaAlias')
        rmFila = request.POST.get('rmFila')
        atualizar_fila = request.POST.get('atualizar_fila')
        adicionar_ramal =request.POST.get('adicionar_ramal')
        del_ramal_fila=request.POST.get('del_ramal_fila')

        if del_ramal_fila is not None:
            rm_ramal_fila = del_ramal_fila.split(' ')
            filas=listarLike('fila', TabelaSipPeers,'name',rm_ramal_fila[0])
            ex_fila=filas[0].replace(rm_ramal_fila[1],'')
            updateONE(TabelaSipPeers,'fila',ex_fila,'name',rm_ramal_fila[0])


        if atualizar_fila:
            idFila = request.POST.get('idFila')
            list_do_upt =[request.POST.get('nome_da_fila'),request.POST.get('estrategia'),request.POST.get('anuncio'),
                          request.POST.get('toque')]
            list_fila_atual =[buscaExata('alias',TabelaFilas,'id',idFila),buscaExata('strategy',TabelaFilas,'id',
                            idFila),buscaExata('announce',TabelaFilas,'id',idFila),buscaExata('timeout',TabelaFilas,'id',idFila)]
            #col_par para achar o indice que corresponde a coluna para ser alterada
            col_par=0
            #colunas para ser alterada
            colunas_upt= ['alias','strategy','announce','timeout']
            for i, n in zip(list_do_upt,list_fila_atual):
                if i == n:
                    pass
                elif i is None and n == 'no':
                    pass
                elif i == 'on' and n == 'yes':
                    pass
                elif i == '3' and n == '15':
                    pass
                elif i == '4' and n == '20':
                    pass
                elif i == '5' and n == '25':
                    pass
                else:
                    try:
                        if colunas_upt[col_par] == 'alias':
                            i = i.replace(" ", "_")

                        if colunas_upt[col_par] == 'timeout':
                            i = int(i)*5
                        if colunas_upt[col_par] == 'announce':
                            if i is None:
                                i= 'no'
                            elif i == 'on':
                                i='yes'
                        #print(colunas_upt[col_par])
                        updateONE('filas',colunas_upt[col_par],i,'id',idFila)
                    except Exception as e:
                        print(e)
                #Muda o indice logo muda a coluna
                col_par+=1

        for i in IDFilas:
            SelectFila = request.POST.get(f'fila{i}')
            if SelectFila is not None:
                CtFl=ConteudoFila(str(SelectFila[0]))
                ItensFila=zip(CtFl,CtFl,CtFl)
                return render(request, FilaPage, {'': ItensFila})
        if filaAlias is None and rmFila is not None :
            ramais=listarLike('name', TabelaSipPeers,'fila',rmFila)
            filas=listarLike('fila', TabelaSipPeers,'fila',rmFila)
            for i,n in zip(ramais,filas):
                ex_fila=n.replace(rmFila,'')
                updateONE(TabelaSipPeers,'fila',ex_fila,'name',i)
            updateToNull(TabelaFilas,'alias','id',rmFila)



            return redirect(filaview)
        if any(i is not None for i in[filaAlias,atualizar_fila,adicionar_ramal]):
            if adicionar_ramal is not None:
                ramal_adicionar = request.POST.get('ramal_adicionar')
                filas_atuais=buscaExata('fila',TabelaSipPeers,'name',ramal_adicionar)
                updateONE(TabelaSipPeers,'fila',str(filas_atuais)+str(adicionar_ramal),'name',ramal_adicionar)
                idFila = adicionar_ramal
            if filaAlias is not None:
                idFila = filaAlias.split(' ')[0]
            lista_ramais = listarUniColAll('name', TabelaSipPeers, 'id')
            lista_filas_atual = listarLike('name', TabelaSipPeers, 'fila',idFila)
            nome_da_fila = buscaExata('alias',TabelaFilas,'id',idFila)
            estrategia_atual = buscaExata('strategy',TabelaFilas,'id',idFila)
            toque_atual = buscaExata('timeout',TabelaFilas,'id',idFila)
            anuncio_atual = buscaExata('announce',TabelaFilas,'id',idFila)
            if toque_atual <= 15:
                toque_atual = 3
            if toque_atual >= 16 and toque_atual <= 24:
                toque_atual = 4
            if toque_atual >= 25:
                toque_atual = 5
            #ramais_atual = buscaExata('alias','filas','id',filaAlias[0])
            NomeFilas = listarUniColAll('alias', TabelaFilas, 'id')
            FilasGeral = zip(IDFilas, NomeFilas)
            return render(request, FilaPage, {'idFila':idFila,'FilasGeral': FilasGeral, 'nome_da_fila': nome_da_fila,
                'estrategia_atual':estrategia_atual, 'toque_atual':toque_atual,'anuncio_atual':anuncio_atual,'lista_filas_atual':lista_filas_atual,
                'estrategias':estrategias, 'toques':toques,'lista_ramais':lista_ramais })
        return redirect(filaview)

@login_required(login_url='login')
def gruposview(request):
    lista_grupos = listarUniColAll('grupo', TabelaGrupos, 'id')
    if request.method == 'GET':

        return render(request, GruposPage, {'lista_grupos':lista_grupos,'aba_grupos':'btn-active'})
    else:
        btn_grupo=request.POST.get('btn_grupo')
        adicionar_grupo=request.POST.get('adicionar_grupo')
        adicionar_ramal=request.POST.get('adicionar_ramal')
        del_ramal_grupo=request.POST.get('del_ramal_grupo')
        del_btn_grupo=request.POST.get('del_btn_grupo')


        if del_btn_grupo is not None:
            idGrupo = buscaExata('id', TabelaGrupos, 'grupo', del_btn_grupo)
            for i in listarLike('name',TabelaSipPeers,'pickupgroup',idGrupo):
                lista_grupos_atual = []
                for g in buscaExata('pickupgroup',TabelaSipPeers,'name',i).split(','):
                    if g not in ('','None',str(idGrupo), None):
                        lista_grupos_atual.append(g)
                updateONE(TabelaSipPeers,'pickupgroup',','.join(lista_grupos_atual),'name',i)
                updateONE(TabelaSipPeers, 'callgroup', ','.join(lista_grupos_atual), 'name', i)
            deletarBanco(TabelaGrupos,'id',idGrupo)

                #
                #
                #if str(idGrupo) in buscaExata('pickupgroup',TabelaSipPeers,'name',i).split(','):
                #    lista_grupos_atual.append(i)
            #lista_ramais = listarUniColAll('name', TabelaSipPeers, 'id')

            pass

        if del_ramal_grupo is not None:
            idGrupo = buscaExata('id', TabelaGrupos, 'grupo', request.POST.get('grupo_rm'))
            gruposR = buscaExata('pickupgroup',TabelaSipPeers,'name',del_ramal_grupo).split(',')
            novoG=[]
            for i in gruposR:
                if str(i) != str(idGrupo):
                    novoG.append(i)
            novoG=','.join(novoG)
            updateONE(TabelaSipPeers,'pickupgroup',novoG,'name',del_ramal_grupo)
            gruposR = buscaExata('callgroup',TabelaSipPeers,'name',del_ramal_grupo).split(',')
            novoG=[]
            for i in gruposR:
                if str(i) != str(idGrupo):
                    novoG.append(i)
            novoG=','.join(novoG)
            updateONE(TabelaSipPeers,'callgroup',novoG,'name',del_ramal_grupo)
            btn_grupo = request.POST.get('grupo_rm')

        if adicionar_ramal:
            ramal_adicionar=request.POST.get('ramal_adicionar')
            if ramal_adicionar is not None:
                idGrupo = buscaExata('id', TabelaGrupos, 'grupo', request.POST.get('add_grupo'))
                pickupG=buscaExata('pickupgroup',TabelaSipPeers,'name',ramal_adicionar)
                callG = buscaExata('callgroup', TabelaSipPeers, 'name', ramal_adicionar)
                updateONE(TabelaSipPeers,'pickupgroup',str(pickupG) + ',' + str(idGrupo),'name',ramal_adicionar)
                updateONE(TabelaSipPeers, 'callgroup', str(callG) + ',' + str(idGrupo), 'name', ramal_adicionar)
            btn_grupo = request.POST.get('add_grupo')

        if adicionar_grupo:
            grupo=request.POST.get('grupo')
            if grupo != '':
                grupo=grupo.replace(' ','_')

                incluirRamal(TabelaGrupos,['grupo'],[str(grupo)])

        if btn_grupo is not None:
            idGrupo = buscaExata('id',TabelaGrupos,'grupo',btn_grupo)
            lista_grupos_atual = []
            #adiciona apenas os ramais que os grupos podem ser separados por virgula
            for i in listarLike('name',TabelaSipPeers,'pickupgroup',idGrupo):
                if str(idGrupo) in buscaExata('pickupgroup',TabelaSipPeers,'name',i).split(','):
                    lista_grupos_atual.append(i)
            lista_ramais = listarUniColAll('name', TabelaSipPeers, 'id')
            return render(request, GruposPage, {'lista_grupos':lista_grupos,'btn_grupo':btn_grupo,
                                                'lista_ramais':lista_ramais,'lista_grupos_atual':lista_grupos_atual,
                                                'aba_grupos':'btn-active'})

        return redirect(gruposview)

@login_required(login_url='login')
def teste(request):
    if request.method == POST:
        #file = request.FILES['file']
        #new_file = UploadedFile(file=file)
        #new_file.save()
        #fs = FileSystemStorage()
        #fs.save(file.name, file)

        audio_file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, '', audio_file.name)
        with open(file_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        return render(request, 'pbx/teste.html')
    else:

        return render(request, AudioPage,{'aba_audio':'btn-active'})

#Funções dentro da pagina
def PagRamaisListas():
        lista_de_ramais = listarRamais()
        lista_de_grupos = listarUniColAll('grupo', TabelaGrupos,'grupo')
        lista_de_troncos = listarUniColAll('did', TabelaDids, 'did')
        return [lista_de_ramais,lista_de_grupos,lista_de_troncos]












