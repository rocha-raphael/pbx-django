from django.db import connections
from django.http import HttpResponse

#variaveis globais
cursor=cursor = connections['ipbx'].cursor()

#funções acessorias usada por outras funções
def listarFetchall(listacompleta):
    listagem=[]
    for i in listacompleta:
        listagem.append(i)
    return listagem


#Querys
########################################################################################################################
def listarRamais():
    listar = 'select id, name, fullname, context, pickupgroup, trunkname, gravar, secret, ipaddr  from sippeers order by name'
    cursor.execute(listar)
    listacompleta = cursor.fetchall()

    conteudo=[]
    for i in listacompleta:
        conteudo.append(list(i))
    for i in conteudo:
        grupo=buscaExata('grupo','grupos','id',i[4])
        i[4]=grupo
        if grupo is None or grupo == "":
            i[4] = "NA"
        for n in range(len(i)):
            if i[n] is None:
                i[n]=""
    return conteudo
def listar_edicao(id):
    listar = f'select id, name, fullname, context, pickupgroup, trunkname, gravar, secret, ipaddr  from sippeers where id =\'{id}\''
    cursor.execute(listar)
    listacompleta = cursor.fetchall()
    conteudo=[]
    grupo = buscaExata('grupo', 'grupos', 'id', listacompleta[0][4])
    for i in range(len(listacompleta[0])):
        if i == 4:
            conteudo.append(grupo)
        elif listacompleta[0][i] is None:
            conteudo.append("")
        else:
            conteudo.append(listacompleta[0][i])
    return conteudo

def descricao(tabela):
    cursor.execute(f'desc {tabela}')
    return cursor.fetchall()

def listarFila():
    listar = 'select alias, strategy,announce,music,timeout from filas where alias is not NULL order by id'
    cursor.execute(listar)
    listacompleta = cursor.fetchall()
    return listarFetchall(listacompleta)

def ConteudoFila(id):
    listar = f'select alias, strategy,announce,music,timeout from filas where id = \'{id}\''
    cursor.execute(listar)
    listacompleta = cursor.fetchall()
    conteudo=[]
    for i in listacompleta:
        for n in i:
            conteudo.append(n)
    return conteudo

#incluir valor na tabela
def incluirRamal(tabela,colunas,valores):
    try:
        colunas = ','.join(colunas)
        valoresAll = valores[0]
        for i in range(len(valores)):
            op = i + 1
            if op == len(valores):
                break
            valoresAll = valoresAll + '\',\'' + str(valores[op])
        valoresAll = '\'' + valoresAll + '\''
        Inserir = f'insert into {tabela} ({colunas}) values ({valoresAll})'
        cursor.execute(Inserir)
        cursor.commit()
    except  Exception as erro:
        return HttpResponse(f'{erro}')

#Selecionar todos ids da tabela
def listarID(tabela):
    listar = f'select id from {tabela} order by id'
    cursor.execute(listar)
    listacompleta = cursor.fetchall()
    listacompleta=listarFetchall(listacompleta)
    listaID=[]
    for i in listacompleta:
        listaID.append(i[0])
    return listaID

#Selecionar todos itens de uma unica coluna de uma tabela
def listarUniColAll(coluna,tabela,order):
    listar = f'select {coluna} from {tabela} order by {order}'
    cursor.execute(listar)
    listacompleta = cursor.fetchall()
    listacompleta=listarFetchall(listacompleta)
    lista=[]
    for i in listacompleta:
        if i[0] is not None:
            lista.append(i[0])
        elif i[0] == "":
            lista.append("Vazio")
        else:
            lista.append("Vazio")
    return lista

def listarLike(coluna,tabela,wcoluna,like):
    listar = f'select {coluna} from {tabela} where {wcoluna} like \'%{like}%\''
    cursor.execute(listar)
    listacompleta = cursor.fetchall()
    listacompleta=listarFetchall(listacompleta)
    lista=[]
    for i in listacompleta:
        if i[0] is not None:
            lista.append(i[0])
        elif i[0] == "":
            lista.append("Vazio")
        else:
            lista.append("Vazio")
    return lista

#Buscar uma celula exata
def buscaExata(coluna, tabela, colunaX,colunaY):
    try:
        listar = f'select {coluna} from {tabela} where {colunaX} = \'{colunaY}\''
        cursor.execute(listar)
        listacompleta = cursor.fetchall()
        listacompleta = listarFetchall(listacompleta)
        lista = []
        for i in listacompleta:
            if i[0] is not None:
                lista.append(i[0])
            elif i[0] == "":
                lista.append("Vazio")
            else:
                lista.append("Vazio")
        return lista[0]
    except Exception as e:
        print(e)

#PASSAR LISTA DE UPDATE
def AtualizarRamais(tabela, listaColuna, listaAtual, Wcoluna, Icoluna):
    try:
        for c, a in zip(listaColuna,listaAtual):
            update = f'update {tabela} set {c} = \'{a}\' where {Wcoluna} =  \'{Icoluna}\''
            cursor.execute(update)
    except Exception as e:
        print(e)

def updateONE(tabela, setC, Inovo, Wcoluna, Icoluna):
    try:
        update = f'update {tabela} set {setC} = \'{Inovo}\' where {Wcoluna} =  \'{Icoluna}\''
        cursor.execute(update)
    except Exception as e:
        print(e)

def updateToNull(tabela, setC, Wcoluna, Icoluna):
    try:
        update = f'update {tabela} set {setC} = Null where {Wcoluna} =  \'{Icoluna}\''
        cursor.execute(update)
    except Exception as e:
        print(e)

#DELETAR ALGO NA TABELA
def deletarBanco(nome_da_tabela,nome_da_coluna,valor_da_coluna):
    try:
        delete = f'DELETE FROM {nome_da_tabela} WHERE {nome_da_coluna} = {valor_da_coluna}'
        cursor.execute(delete)
    except Exception as e:
        print(e)

def tiposEnum(nome_da_tabela,nome_da_coluna):
    try:
        cursor.execute(f"DESCRIBE {nome_da_tabela} {nome_da_coluna}")
        desc = cursor.fetchall()
        desc = desc[0][1]
        if desc.find('enum(') == -1:
            return None
        else:
            desc = desc.replace('enum(','')
            desc = desc.replace(')', '')
            desc = desc.replace('\'', '')
            desc = desc.split(',')
            return desc

    except Exception as e:
        print(e)

class Select:
    def __init__(self, colunas, tabela, onde, igual_parecido, com_oq, ordenar):
        pass
