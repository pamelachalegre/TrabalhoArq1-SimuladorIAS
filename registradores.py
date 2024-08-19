'''
TRABALHO ARQUITETURA E ORGANIZAÇÃO DE COMPUTADORES 1
ALUNA: Ana Paula Loureiro Crippa - RA 137304
ALUNA: Maria Eduarda de Mello Policante - RA 134539
ALUNA: Pâmela Camilo Chalegre - RA 134241
'''

import io

#registradores de manipulam dados:
AC: int = 0 #acumulador
MQ: int = 1 #multiplicador
R: int #resto da divisao
C: int # Carry out (1: houve carry; 2: não houve carry)
Z: int # Resultado zero (-1: resultado negativo; 0: resultado igual a zero; 1: resultado positivo)
#registradores que armazenam partes da instrucao:
PC: str
IR: str
MAR: str
MBR: int
GERAL_A: str = ''
GERAL_B: str = ''
GERAL_C: str = ''
OFFSET_ARQ: int #variavel para manipulação do arquivo

def contar_memoria(arq: io.TextIOWrapper) -> tuple[list[str], int]:
    global PC
    '''conta quantas linhas tem o arquivo'''
    linha = arq.readline()
    memoria_volatil_dados: list[str] = []
    while linha != '\n': #a memória se separa das instrucoes
        memoria_volatil_dados.append(linha) #adiciona o dado lido a memoria de dados
        linha = arq.readline()
    return memoria_volatil_dados, arq.tell() #offset -> onde vão começar as instruções reais

def buscar_operando(memoria_volatil: list[str], referencia: str) -> int:
    '''busca o endereco na memoria e retorna o dado que esta nele -> se for endereçamento direto. Caso seja imediato, retorna o proprio dado'''
    if referencia[:2] == '0X': #se for um endereco -> endereçamento direto
        i = 0
        palavra = memoria_volatil[i].strip('\n').split(sep=' ') #pega a palavra aramazenada e divide endereco do dado
        while palavra[0] != referencia and i < len(memoria_volatil) - 1:
            i += 1
            palavra = memoria_volatil[i].strip('\n').split(sep=' ')
        
        if palavra[0] == referencia: 
            return int(palavra[1])
        else:
            raise ValueError('Endereço não encontrado!')
    else: #se for enderecamento imediato -> o operando faz parte da instrucao
        return int(referencia)

def buscar_registrador(memoria_volatil: list[str], parametro: str) -> int:
    global MQ, GERAL_A, GERAL_B, GERAL_C, MBR
    if parametro == 'A':
        return GERAL_A
    elif parametro == 'B':
        return GERAL_B
    elif parametro == 'C':
        return GERAL_C
    elif parametro == 'MQ':
        return MQ
    else:
        MBR = buscar_operando(memoria_volatil, parametro)
        print("MBR:", MBR)
        return MBR

def atualizar_registrador(parametro: str, valor: int):
    global MQ, GERAL_A, GERAL_B, GERAL_C
    if parametro == 'A':
        GERAL_A = valor
    elif parametro == 'B':
        GERAL_B = valor
    elif parametro == 'C':
        GERAL_C = valor
    elif parametro == 'MQ':
        MQ = valor

def executar_load(memoria_volatil: list[str], instrucao: list[str]) -> None: 
    ''' LOAD X | LOAD X, Y
    Carrega o valor da memória no acumulador (AC) ou em outro registrador especificado. '''
    global MBR, AC, MQ, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #LOAD X : AC <- X
        MBR = buscar_operando(memoria_volatil, instrucao[1]) #busca o dado que esta no endereco
        print("MBR:", MBR)
        AC = MBR #AC recebe o valor pego na memória por MBR
        print("AC =", AC)
    else: #LOAD X, Y : X <- Y
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2]) #busca o dado que esta no endereco
        print("MBR:", MBR)
        if registrador == 'MQ':
            MQ = MBR
            print("MQ =", MQ)
        elif registrador == 'A':
            GERAL_A = MBR
            print("Registrador A =", GERAL_A)
        elif registrador == 'B':
            GERAL_B = MBR
            print("Registrador B =", GERAL_B)
        elif registrador == 'C':
            GERAL_C = MBR
            print("Registrador C =", GERAL_C)

def executar_mover(instrucao: list[str]) -> None:
    ''' MOV X | MOV X, Y 
    Move dados de um registrador para outro. '''
    global AC, MQ, GERAL_A, GERAL_B, GERAL_B, GERAL_C
    registrador = instrucao[1].strip(',') #Registrador X (elemento obrigatório)
    if len(instrucao) == 2: #MOV X : AC <- X (o valor de X vai para o AC)
        AC = buscar_registrador([], registrador) #não há busca por operandos na memória
        print(f"AC = {AC} (AC <- {registrador})")
    else: #MOV X, Y : X <- Y (o valor de Y vai para X)
        fonte = instrucao[2] #o valor da FONTE será movido para o registrador X
        BARRA_DADOS = buscar_registrador([], fonte)
        atualizar_registrador(registrador, BARRA_DADOS) #Coloca o valor posto em "barra_dados" no registrador X correto
        print(f"{registrador} = {BARRA_DADOS} ({registrador} <- {fonte})")
        
def executar_soma(memoria_volatil: list[str], instrucao: list[str]):
    ''' ADD X | ADD X, Y
    Soma um dado ao acumulador ou a outro registrador especificado.'''
    global AC, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2: #ADD X : AC <- AC + X
        BARRA_DADOS = buscar_registrador(memoria_volatil, parametro)
        print("AC =", AC, "+", BARRA_DADOS, end=' ')
        AC += BARRA_DADOS
        print("=", AC)
    else: #ADD X, Y : X <- X + Y
        USO_ULA = buscar_registrador(memoria_volatil, parametro)
        BARRA_DADOS = buscar_registrador(memoria_volatil, instrucao[2])
        print(f"Registrador {parametro} = {USO_ULA} + {BARRA_DADOS}", end=' ')
        USO_ULA += BARRA_DADOS
        print("=", USO_ULA)
        atualizar_registrador(parametro, USO_ULA)

def executar_subtracao(memoria_volatil: list[str], instrucao: list[str]):
    ''' SUB X | SUB X, Y 
    Subtrai um dado de AC ou outro registrador especificado.'''
    global AC, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2: #SUB X : AC <- AC - X
        BARRA_DADOS = buscar_registrador(memoria_volatil, parametro)
        print("AC =", AC, "-", BARRA_DADOS, end=' ')
        AC -= MBR
        print("=", AC)
    else:
        USO_ULA = buscar_registrador(memoria_volatil, parametro)
        BARRA_DADOS = buscar_registrador(memoria_volatil, instrucao[2])
        print(f"Registrador {parametro} = {USO_ULA} - {BARRA_DADOS}", end=' ')
        USO_ULA -= BARRA_DADOS
        atualizar_registrador(parametro, USO_ULA)
        print("=", USO_ULA)

def executar_multiplicacao(memoria_volatil: list[str], instrucao: list[str]):
    ''' MULT X | MULT X, Y
    Multiplica um dado X pelo MQ ou outro registrador especificado.'''
    global MQ, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2: #se só tiver um elemento, soma-se com o AC
        BARRA_DADOS = buscar_registrador(memoria_volatil, parametro)
        print("MQ =", MQ, "*", MBR, end=' ')
        MQ *= MBR
        print("=", MQ)
    else:
        USO_ULA = buscar_registrador(memoria_volatil, parametro)
        BARRA_DADOS = buscar_registrador(memoria_volatil, instrucao[2])
        print(f"Registrador {parametro} = {USO_ULA} * {BARRA_DADOS}", end=' ')
        USO_ULA *= BARRA_DADOS
        atualizar_registrador(parametro, USO_ULA)
        print("=", USO_ULA)

def executar_divisao(memoria_volatil: list[str], instrucao: list[str]):
    ''' DIV X | DIV X, Y
    Divide o AC ou um registrador específico (Y) por um dado X'''
    global AC, R, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2:
        BARRA_DADOS = buscar_registrador(memoria_volatil, parametro)
        if BARRA_DADOS == 0:
            raise ValueError("Divisão por 0.")
        else:
            print(f"AC = {AC} / {BARRA_DADOS}")
            R = AC % BARRA_DADOS
            AC //= BARRA_DADOS
            print(f"= {AC} (com resto R = {R})")
    else:
        USO_ULA = buscar_registrador(memoria_volatil, parametro)
        BARRA_DADOS = buscar_registrador(memoria_volatil, instrucao[2])
        if BARRA_DADOS == 0:
            raise ValueError("Divisão por 0.")
        else:
            print(f"{parametro} = {USO_ULA} / {BARRA_DADOS}")
            R = USO_ULA % BARRA_DADOS
            USO_ULA //= BARRA_DADOS
            print(f"= {USO_ULA} (com resto R = {R})")
            atualizar_registrador(parametro, USO_ULA)

def executar_escrita(memoria_volatil: list[str], instrucao: list[str], arq: io.TextIOWrapper):
    if len(instrucao) == 2: #tem apenas um dado a ser escrito na memoria.
        MBR = instrucao[1] #dado a ser escrito na memoria.
    print("Escrita feita!")

def executar_salto(arq: io.TextIOWrapper, instrucao: list[str], offset_inst: int):
    ''' JUMP X : PC <- X
    Executa um salto na execução sequencial das instruções.'''
    global PC, OFFSET_ARQ
    PC = instrucao[1] #pular para a rotina de instrução.
    print("Instrução de desvio -> PC:", PC) #novo endereço
    arq.seek(offset_inst) #vai pro começo das instruções
    OFFSET_ARQ = arq.tell() #armazena o offset novo
    volta = arq.readline().strip('\n') #primeiro endereco do PC -> 0X0A
    contar = volta
    while contar != PC: #compara se chegamos no endereco desejado
        OFFSET_ARQ = arq.tell() #pega o offset daquele endereco
        contar = str(hex(int(contar, 16) + 1)).upper() #incrementa
        volta = arq.readline().strip('\n') #le mais uma linha
        #ao fim, o offset do inicio da linha correspondente ao endereço de PC é atualizado e levado para a leitura das proximas instruções

def executar_salto_zero(arq: io.TextIOWrapper, instrucao: list[str], offset_inst: int):
    ''' JUMP+ X : PC <- X (A = 0)
    Executa um salto na execução sequencial das instruções se o AC for 0.'''
    global PC, AC, OFFSET_ARQ
    if AC == 0:
        PC = instrucao[1] #pular para a rotina de instrução.
        print("Instrução de desvio -> PC:", PC) #novo endereço
        arq.seek(offset_inst) #vai pro começo das instruções
        OFFSET_ARQ = arq.tell() #armazena o offset novo
        volta = arq.readline().strip('\n') #primeiro endereco do PC -> 0X0A
        contar = volta
        while contar != PC: #compara se chegamos no endereco desejado
            OFFSET_ARQ = arq.tell() #pega o offset daquele endereco
            contar = str(hex(int(contar, 16) + 1)).upper() #incrementa
            volta = arq.readline().strip('\n') #le mais uma linha
        #ao fim, o offset do inicio da linha correspondente ao endereço de PC é atualizado e levado para a leitura das proximas instruções
    else:
        print(f"Instrução não executada! Condição não respeitada! (AC = {AC})")

def instrucoes(memoria_volatil: list[str], instrucao: str, arq: io.TextIOWrapper, offset_inst: int) -> None:
    instrucao = instrucao.split(' ')
    IR = instrucao[0]
    print("Instrução atual -> IR:", IR) #mostra qual instrução está sendo executada
    if IR == 'LOAD': #identifica a instrução
        executar_load(memoria_volatil, instrucao)
    elif IR == 'MOV':
        executar_mover(instrucao)
    elif IR == 'ADD':
        executar_soma(memoria_volatil, instrucao)
    elif IR == 'SUB':
        executar_subtracao(memoria_volatil, instrucao)
    elif IR == 'MULT':
        executar_multiplicacao(memoria_volatil, instrucao)
    elif IR == 'DIV':
        executar_divisao(memoria_volatil, instrucao)
    elif IR == 'JUMP':
        executar_salto(arq, instrucao, offset_inst)
    elif IR == 'JUMP+':
        executar_salto_zero(arq, instrucao, offset_inst)
    elif IR == 'STOR': #essa não tá feita
        executar_escrita(memoria_volatil, instrucao, arq)

def le_instrucao(arq: io.TextIOWrapper) -> tuple[str, int]:
    global PC, MAR
    '''pior que ela leu. fiquei em choque'''
    MAR = PC #endereço da instrução a ser executada -> apontada por PC
    print("Endereço da instrução atual -> MAR:", MAR)
    arq.seek(OFFSET_ARQ, 0) #pula a memoria e as instruções já executadas
    instrucao = arq.readline().strip('\n') # le a próxima instrução
    PC = str(hex(int(PC, 16) + 1)).upper() #incrementa o pc (sim, joguei no google como somar está porra 1 a 1)
    return instrucao, arq.tell() #instrução lida, pc incrementado, offset da proxima instrucao (próxima linha)

def main():
    try:
        global PC, IR, OFFSET_ARQ, GERAL_A, GERAL_B, GERAL_C, MBR, AC, MQ
        arq = input("\nDigite o nome (com extensão .txt) do arquivo de memória a ser executado: ")
        arq = open(arq, 'r+')
        memoria_volatil, OFFSET_ARQ = contar_memoria(arq) #retorna os elementos da memória em forma de lista, pega o primeiro valor de PC (primeira linha pós memória) e o offset da próxima linha
        offset_inst = OFFSET_ARQ #variável para o primeiro offset das instruções

        PC = arq.readline().strip('\n') #primeiro endereco do PC -> primeira linha pós-memória (tira o \n da quebra)
        OFFSET_ARQ = arq.tell() #offset após ler o PC
        print("Endereço da próxima instrução -> PC:", PC, "\n") #printa o primeiro endereco de PC
        for i in range(11):
            IR, OFFSET_ARQ = le_instrucao(arq) #busca a proxima instrução (do endereço de PC) -> carrega em IR, incrementa PC e retorna o offset da próxima linha
            instrucoes(memoria_volatil, IR, arq, offset_inst) #usam os dados da "memoria_volatil" para executar a instrução de "IR".
            print("Endereço da próxima instrução -> PC: ", PC, "\n")

        arq.close()

    except FileNotFoundError:
        print(f"\nArquivo '{arq}' não encontrado.\n")

if __name__ == '__main__':
    main()
