import sys

TODO_FILE = '/home/CIN/ggm/Downloads/todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"
MAGENTA = "\033[0;35m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

def printCores(texto, cor) :
  print(cor + texto + RESET)

def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True

def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  elif horaMin[:2] < '00' or horaMin[:2] > '23':
      return False
  elif horaMin[2:] < '00' or horaMin[2:] > '59':
      return False
  else:
    return True

def verificaExistencia(objeto, lista):
    if lista == []:
        return False
    else:
        head = lista.pop(0)
        if head == objeto:
            return True
        else:
            return verificaExistencia(objeto, lista)

def calendario(dia, mes):
    mesesTrintaEUm = ['01', '03', '05', '07', '08', '10', '12']
    mesesTrinta = ['04', '06', '09', '11']
    mesesVinteNove = ['02']
    if verificaExistencia(mes, mesesTrintaEUm) == True:
        if int(dia) > 31:
            return False
    elif verificaExistencia(mes, mesesTrinta) == True:
        if int(dia) > 30:
            return False
    elif verificaExistencia(mes, mesesVinteNove) == True:
        if int(dia) > 29:
            return False
    else:
        return True
         
def dataValida(data) :
    if len(data) != 8 or not soDigitos(data):
        return False
    elif data[:2] < '01' or data[:2] > '31':
        return False
    elif data[2:4] < '01' or data[2:4] > '12':
        return False
    elif calendario(data[:2], data[2:4]) == False:
        return False
    else:
        return True

def projetoValido(proj):
    if len(proj) < 2 or proj[0] != '+':
        return False
    else:
        return True

def contextoValido(cont):
    if len(cont) < 2 or cont[0] != '@':
        return False
    else:
        return True

def prioridadeValida(pri):
    if len(pri) != 3 or pri[0] != '(' or pri[2] != ')':
        return False
    elif pri[1].lower() < 'a' or pri[1].lower() > 'z':
        return False
    else:
        return True

def lerArquivo(arquivo, modo):
    arq = open(arquivo, modo)
    return arq.readlines()

def organizar(linhas):
  itens = []
  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    
    l = l.strip()
    tokens = l.split()
    
    for x in tokens:
        if dataValida(x) == True:
            data = x
        elif horaValida(x) == True:
            hora = x
        elif prioridadeValida(x) == True:
            pri = x
        elif contextoValido(x) == True:
            contexto = x
        elif projetoValido(x) == True:
            projeto = x
        else:
            desc = desc + x + ' '
    desc = desc.strip()

    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens
    
def adicionar(novaAtividade):
    data = '' 
    hora = ''
    prioridade = ''
    descricao = ''
    contexto = ''
    projeto = ''
    novaAtividade = novaAtividade.split()
    for x in novaAtividade:
        if dataValida(x) == True:
            data = x
        elif horaValida(x) == True:
            hora = x
        elif prioridadeValida(x) == True:
            prioridade = x
        elif contextoValido(x) == True:
            contexto = x
        elif projetoValido(x) == True:
            projeto = x
        else:
            descricao = descricao + x + ' '
    descricao = descricao.strip()
    if descricao  == '' :
      print('Só serão aceitas atividades com pelo menos uma descrição.')
      return
    novaAtividade = [data, hora, prioridade, descricao, contexto, projeto]
    atividade = ''
    for x in novaAtividade:
        if x != '':
            atividade += x + ' '
    try:
        fp = open(TODO_FILE, 'a')
        fp.write(atividade + "\n")
        fp.close()
        print("Atividade adicionada! ^-^")
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False
    return

def inverter(data):
    data = data[4:] + data[2:4] + data[:2]
    return data

def ordenarPorData(itens):
    for x in itens: 
        aux = 0
        while aux < len(itens) - 1:
            if inverter(itens[aux][1][0]) > inverter(itens[aux + 1][1][0]):
                temp = itens[aux]
                itens[aux] = itens[aux + 1]
                itens[aux + 1] = temp
            aux += 1
    datasVazias = []
    contadorVazio = 0
    for x in itens:
        if x[1][0] == '':
            datasVazias.append(x)
            contadorVazio += 1
    while contadorVazio != 0:
        itens.pop(0)
        contadorVazio = contadorVazio - 1
    itens += datasVazias
    return itens

def ordenarPorDataHora(itens):
    itens = ordenarPorData(itens)
    for x in itens:
        aux = 0
        while aux < len(itens) - 1:
            if itens[aux][1][0] == itens[aux + 1][1][0] and itens[aux][1][1] > itens[aux + 1][1][1] and itens[aux + 1][1][1] != '':
                temp = itens[aux]
                itens[aux] = itens[aux + 1]
                itens[aux + 1] = temp
            aux += 1
    return itens

def ordenarPorPrioridade(itens):
    for x in itens:
        aux = 0
        while aux < len(itens) - 1:
            if itens[aux][1][2].upper() > itens[aux + 1][1][2].upper():
                temp = itens[aux]
                itens[aux] = itens[aux + 1]
                itens[aux + 1] = temp
            aux += 1
    prioridadesVazias = []
    contadorVazio = 0
    for x in itens:
        if x[1][2] == '':
            prioridadesVazias.append(x)
            contadorVazio += 1
    while contadorVazio != 0:
        itens.pop(0)
        contadorVazio = contadorVazio - 1
    itens += prioridadesVazias
    return itens

def ordenar(itens):
  itens = ordenarPorDataHora(itens)
  itens = ordenarPorPrioridade(itens)
  return itens

def colocarBarra(data):
  data = data[:2] + '/' + data[2:4] + '/' + data[4:]
  return data

def colocarDoisPontos(hora):
  hora = hora[:2] + ':' + hora[2:]
  return hora

def removerVazio(atividades):
    aux = 0
    while aux < len(atividades):
        i = 0
        extrasDHP = ''
        extrasCP = ''
        while i < len(atividades[aux][1]):
            if atividades[aux][1][i] != '' and dataValida(atividades[aux][1][i]):
                extrasDHP += colocarBarra(atividades[aux][1][i]) + ' '
            elif atividades[aux][1][i] and horaValida(atividades[aux][1][i]):
                extrasDHP += colocarDoisPontos(atividades[aux][1][i]) + ' '
            elif atividades[aux][1][i] and prioridadeValida(atividades[aux][1][i]):
                extrasDHP += atividades[aux][1][i] + ' '
            elif atividades[aux][1][i] != '' and contextoValido(atividades[aux][1][i]) or projetoValido(atividades[aux][1][i]):
                extrasCP += atividades[aux][1][i] + ' '
            i += 1
        novaString = extrasDHP + ' ' + atividades[aux][0] + ' ' + extrasCP
        novaString.strip()
        atividades[aux] = novaString
        aux += 1
    return atividades
    
    

def listar():
  arquivo = open(TODO_FILE, 'r')
  atividades = arquivo.readlines()
  atividades = organizar(atividades)
  atividadesSemOrdenar = atividades[:]
  atividades = ordenar(atividades)
  atividades = removerVazio(atividades)
  atividadesSemOrdenar = removerVazio(atividadesSemOrdenar)
  indices = []
  for x in atividades:
      aux = 0
      while x != atividadesSemOrdenar[aux]:
          aux += 1
      indices.append(aux)
  cont = 0
  atvOrganizadas = organizar(atividades[:])
  while cont < len(indices):
      if atvOrganizadas[cont][1][2] == '(A)' or atvOrganizadas[cont][1][2] == '(a)':
        printCores(str(indices[cont]) + ' ' + atividades[cont], RED + BOLD)
      elif atvOrganizadas[cont][1][2] == '(B)' or atvOrganizadas[cont][1][2] == '(b)':
        printCores(str(indices[cont]) + ' ' + atividades[cont], YELLOW)
      elif atvOrganizadas[cont][1][2] == '(C)' or atvOrganizadas[cont][1][2] == '(c)':
        printCores(str(indices[cont]) + ' ' + atividades[cont], GREEN)
      elif atvOrganizadas[cont][1][2] == '(D)' or atvOrganizadas[cont][1][2] == '(d)':
        printCores(str(indices[cont]) + ' ' + atividades[cont], BLUE)
      else:
        printCores(str(indices[cont]) + ' ' + atividades[cont], MAGENTA)
      cont += 1

def remover(num):
    copiaDoArquivo = lerArquivo(TODO_FILE, 'r')
    copiaDoArquivo.pop(num)
    novoTodo = open(TODO_FILE, 'w')
    for x in copiaDoArquivo:
        novoTodo.write(x)
    print("Atividade removida! ^-^")
    return

def priorizar(num, prioridade):
    arquivo = lerArquivo(TODO_FILE, 'r')
    copiaDoArquivo = organizar(lerArquivo(TODO_FILE, 'r'))
    copiaDaTarefa = copiaDoArquivo[num]
    temData = False
    temHora = False
    temPrioridade = False
    for x in copiaDaTarefa[1]:
        if dataValida(x) == True:
            temData = True
            break
    for x in copiaDaTarefa[1]:
        if horaValida(x) == True:
            temHora = True
            break
    for x in copiaDaTarefa[1]:
        if horaValida(x) == True:
            temPrioridade = True
            break
    if temData == True and temHora == True and temPrioridade == True:
        arquivo[num] = arquivo[num].strip()
        arquivo[num] = arquivo[num].split()
        arquivo[num][3] = '(' + prioridade + ')'
        arquivo[num] = ' '.join(arquivo[num])
    elif temData == False and temHora == False and temPrioridade == True:
        arquivo[num] = arquivo[num].strip()
        arquivo[num] = arquivo[num].split()
        arquivo[num][1] = '(' + prioridade + ')'
        arquivo[num] = ' '.join(arquivo[num])
    elif temData == False and temHora == False and temPrioridade == False:
        arquivo[num] = arquivo[num].strip()
        arquivo[num] = arquivo[num].split()
        arquivo[num].insert(1, '(' + prioridade + ')')
        arquivo[num] = ' '.join(arquivo[num])
    else:
        arquivo[num] = arquivo[num].strip()
        arquivo[num] = arquivo[num].split()
        arquivo[num][2] = '(' + prioridade + ')'
        arquivo[num] = ' '.join(arquivo[num])
    arquivo[num] += '\n'
    novoTodo = open(TODO_FILE, 'w')
    for x in arquivo:
      novoTodo.write(x)
    print("Prioridade alterada! ^-^")
    return

def fazer(num):
  atividadeFeita = lerArquivo(TODO_FILE, 'r')
  atividadeFeita = atividadeFeita[num]
  arquivo = open(ARCHIVE_FILE, 'a')
  arquivo.write(atividadeFeita)
  arquivo.close
  remover(num)
  print("Marcada como feito! ^-^")
  return 

def processarComandos(comandos) :
    if comandos[1] == ADICIONAR:
        comandos.pop(0)
        comandos.pop(0)
        itemParaAdicionar = ' '.join(comandos)
        adicionar(itemParaAdicionar)
        return
    elif comandos[1] == LISTAR:
      listar()
      return
    
    elif comandos[1] == REMOVER:
        if len(comandos) != 3:
            print("Digite um comando válido: r + número da atividade que deseja remover.")
        if comandos[2] not in range(0, len(lerArquivo(TODO_FILE, 'r'))):
            print("Essa atividade não existe, por favor, digite alguma válida.")
        else:
            remover(comandos[2])
        return

    elif comandos[1] == FAZER:
        if len(comandos) != 3:
            print("Digite um comando válido: f + número da atividade que deseja marcar como feita.")
        if comandos[2] not in range(0, len(lerArquivo(TODO_FILE, 'r'))):
            print("Essa atividade não existe, por favor, digite alguma válida.")
        else:
            fazer(int(comandos[2]))
        return    

    elif comandos[1] == PRIORIZAR:
        if len(comandos) != 4:
            print("Digite um comando válido: p + número da atividade que deseja priorizar.")
        if comandos[2] not in range(0, len(lerArquivo(TODO_FILE, 'r'))):
            print("Essa atividade não existe, por favor, digite alguma válida.")
        else:
            priorizar(int(comandos[2]), comandos[3])
        return
    
    else :
        print("Comando inválido.")

processarComandos(sys.argv)
