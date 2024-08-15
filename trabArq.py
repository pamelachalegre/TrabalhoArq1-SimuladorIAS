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
#registradores que armazenam partes da instrucao:
PC: str
IR: str
MAR: str
MBR: int
GERAL_A: str
GERAL_B: str
GERAL_C: str
OFFSET_ARQ: int #variavel para manipulação do arquivo

def contar_memoria(arq: io.TextIOWrapper) -> tuple[list[str], int]:
    global PC
    '''conta quantas linhas tem o arquivo'''
    linha = arq.readline()
    memoria_volatil_dados: list[str] = []
    while linha != '\n':
        memoria_volatil_dados.append(linha) #adiciona o dado lido a memoria de dados
        linha = arq.readline()
    return memoria_volatil_dados, arq.tell() #offset -> onde vão começar as instruções reais

def buscar_operando(memoria_volatil: list[str], referencia: str) -> int:
    '''busca o endereco na memoria e retorna o dado que esta nele -> se for endereçamento direto. Caso seja imediato, retorna o proprio dado'''
    if referencia[:2] == '0X': #se for um endereco -> endereçamento direto
        i = 0
        palavra = memoria_volatil[i].strip('\n').split(sep=' ') #pega a palavra aramazenada e divide endereco do dado
        while palavra[0] != referencia and i < len(memoria_volatil):
            i += 1
            palavra = palavra = memoria_volatil[i].strip('\n').split(sep=' ')
        
        if i < len(memoria_volatil): 
            return int(palavra[1])
        else:
            print('Endereço não encontrado!')
    else: #se for enderecamento imediato -> o operando faz parte da instrucao
        return int(referencia)
        
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
        if registrador == 'MQ':
            AC = MQ
        elif registrador == 'A':
            AC = GERAL_A
        elif registrador == 'B':
            AC = GERAL_B
        elif registrador == 'C':
            AC = GERAL_C
        print(f"AC = {AC} (AC <- {registrador})")
    else: #MOV X, Y : X <- Y (o valor de Y vai para X)
        fonte = instrucao[2] #o valor da FONTE será movido para o registrador X
        if fonte == 'MQ': #Identifica a fonte Y e coloca seu valor em "bar_dados"
            bar_dados = MQ
        elif fonte == 'A':
            bar_dados = GERAL_A
        elif fonte == 'B':
            bar_dados = GERAL_B
        elif fonte == 'C':
            bar_dados = GERAL_C
        #Coloca o valor posto em "bar_dados" no registrador X correto
        if registrador == 'MQ':
            MQ = bar_dados
        elif registrador == 'A':
            GERAL_A = bar_dados
        elif registrador == 'B':
            GERAL_B = bar_dados
        elif registrador == 'C':
            GERAL_C = bar_dados
        print(f"{registrador} = {bar_dados} ({registrador} <- {fonte})")
        
def executar_soma(memoria_volatil: list[str], instrucao: list[str]):
    ''' ADD X | ADD X, Y
    Soma um dado ao acumulador ou a outro registrador especificado.'''
    global AC, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #ADD X : AC <- AC + X
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        print("MBR:", MBR)
        print("AC =", AC, "+", MBR, end=' ')
        AC += MBR
        print("=", AC)
    else: #ADD X, Y : X <- X + Y
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
        print("MBR:", MBR)
        if registrador == 'A':
            print("Registrador A =", GERAL_A, "+", MBR, end=' ')
            GERAL_A += MBR
            print("=", GERAL_A)
        elif registrador == 'B':
            print("Registrador B =", GERAL_B, "+", MBR, end=' ')
            GERAL_B += MBR
            print("=", GERAL_B)
        elif registrador == 'C':
            print("Registrador C =", GERAL_C, "+", MBR, end=' ')
            GERAL_C += MBR
            print("=", GERAL_C)

def executar_subtracao(memoria_volatil: list[str], instrucao: list[str]):
    ''' SUB X | SUB X, Y 
    Subtrai um dado de AC ou outro registrador especificado.'''
    global AC, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #SUB X : AC <- AC - X
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        print("MBR:", MBR)
        print("AC =", AC, "+", MBR, end=' ')
        AC -= MBR
        print("=", AC)
    else:
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
        print("MBR:", MBR)
        if registrador == 'A':
            print("Registrador A =", GERAL_A, "-", MBR, end=' ')
            GERAL_A -= MBR
            print("=", GERAL_A)
        elif registrador == 'B':
            print("Registrador B =", GERAL_B, "-", MBR, end=' ')
            GERAL_B -= MBR
            print("=", GERAL_B)
        elif registrador == 'C':
            print("Registrador C =", GERAL_C, "-", MBR, end=' ')
            GERAL_C -= MBR
            print("=", GERAL_C)

def executar_multiplicacao(memoria_volatil: list[str], instrucao: list[str]):
    ''' MULT X | MULT X, Y
    Multiplica um dado X pelo MQ ou outro registrador especificado.'''
    global MQ, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #se só tiver um elemento, soma-se com o AC
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        print("MBR:", MBR)
        print("MQ =", MQ, "*", MBR, end=' ')
        MQ *= MBR
        print("=", MQ)
    else:
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
        print("MBR:", MBR)
        if registrador == 'A':
            print("Registrador A =", GERAL_A, "*", MBR, end=' ')
            GERAL_A *= MBR
            print("=", GERAL_A)
        elif registrador == 'B':
            print("Registrador B =", GERAL_B, "*", MBR, end=' ')
            GERAL_B *= MBR
            print("=", GERAL_B)
        elif registrador == 'C':
            print("Registrador C =", GERAL_C, "*", MBR, end=' ')
            GERAL_C *= MBR
            print("=", GERAL_C)

def executar_divisao(memoria_volatil: list[str], instrucao: list[str]):
    ''' DIV X | DIV X, Y
    Divide o AC ou um registrador específico (Y) por um dado X'''
    global AC, R, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #DIV X : AC <- AC // X
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        if MBR != 0:
            print("MBR:", MBR)
            print(f"AC = {AC} / {MBR}", end=' ')
            R = AC % MBR
            AC //= MBR
            print(f"= {AC} (com resto R = {R})")
        else:
            raise ValueError("Divisão por 0.")
    else: #DIV X, Y : X <- X // Y
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
        if MBR != 0:
            print("MBR:", MBR)
            if registrador == 'A':
                print(f"Registrador A = {GERAL_A} / {MBR}", end=' ')
                R = GERAL_A % MBR
                GERAL_A //= MBR
                print(f"= {GERAL_A} (com resto R = {R})")
            elif registrador == 'B':
                print(f"Registrador B = {GERAL_B} / {MBR}", end=' ')
                R = GERAL_B % MBR
                GERAL_B //= MBR
                print(f"= {GERAL_B} (com resto R = {R})")
            elif registrador == 'C':
                print(f"Registrador C = {GERAL_C} / {MBR}", end=' ')
                R = GERAL_C % MBR
                GERAL_C //= MBR
                print(f"= {GERAL_C} (com resto R = {R})")
        else:
            raise ValueError("Divisão por 0.")

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
    ''' JUMP+ X : PC <- X
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
    print("Instrução atual -> IR: ", IR) #mostra qual instrução está sendo executada
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
    print("Endereço da instrução atual -> MAR: ", MAR)
    arq.seek(OFFSET_ARQ, 0) #pula a memoria e as instruções já executadas
    instrucao = arq.readline().strip('\n') # le a próxima instrução
    PC = str(hex(int(PC, 16) + 1)).upper() #incrementa o pc (sim, joguei no google como somar está porra 1 a 1)
    return instrucao, arq.tell() #instrução lida, pc incrementado, offset da proxima instrucao (próxima linha)

def main():
    try:
        global PC, AC, IR, OFFSET_ARQ
        arq = open('memoria.txt', 'r+')
        memoria_volatil, OFFSET_ARQ = contar_memoria(arq) #retorna os elementos da memória em forma de lista, pega o primeiro valor de PC (primeira linha pós memória) e o offset da próxima linha
        offset_inst = OFFSET_ARQ #variável para o primeiro offset das instruções

        PC = arq.readline().strip('\n') #primeiro endereco do PC -> primeira linha pós-memória (tira o \n da quebra)
        OFFSET_ARQ = arq.tell() #offset após ler o PC
        print("Endereço da próxima instrução -> PC:", PC, "\n") #printa o primeiro endereco de PC
        for i in range(13):
            IR, OFFSET_ARQ = le_instrucao(arq) #busca a proxima instrução (do endereço de PC) -> carrega em IR, incrementa PC e retorna o offset da próxima linha
            instrucoes(memoria_volatil, IR, arq, offset_inst) #usam os dados da "memoria_volatil" para executar a instrução de "IR".
            print("Endereço da próxima instrução -> PC: ", PC, "\n")

        arq.close()
    except:
        raise ValueError("Arquivo (memoria.txt) não encontrado.")

if __name__ == '__main__':
    main()