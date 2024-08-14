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
C: int #carry (1, 2)
Z: int #natureza do resultado (-1, 0, 1)
#registradores que armazenam partes da instrucao:
PC: str
IR: str
MAR: str
MBR: int
GERAL_A: str
GERAL_B: str
GERAL_C: str

def contar_memoria(arq: io.TextIOWrapper) -> tuple[list[str], int]:
    global PC
    '''conta quantas linhas tem o arquivo'''
    linha = arq.readline()
    memoria_volatil_dados: list[str] = []
    while linha != '\n':
        memoria_volatil_dados.append(linha) #adiciona o dado lido a memoria de dados
        linha = arq.readline()
    PC = arq.readline().strip('\n') #primeiro endereco do PC -> primeira linha pós-memória (tira o \n da quebra)
    return memoria_volatil_dados, arq.tell() #offset -> onde vão começar as instruções reais

def buscar_operando(memoria_volatil: list[str], referencia: str) -> int:
    '''busca o endereco na memoria e retorna o dado que esta nele -> se for endereçamento direto. Caso seja imediato, retorna o proprio dado'''
    if referencia[:2] == '0x': #se for um endereco -> endereçamento direto
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
        
def executar_load(memoria_volatil: list[str], instrucao: str) -> None: 
    '''EM TESTE!!!! carrega o valor de um endereço de memória no acumulador (AC) ou em outro registrador especificado'''
    global MBR, AC, MQ, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #se só vier com o dado -> usa o AC.
        MBR = buscar_operando(memoria_volatil, instrucao[1]) #busca o dado que esta no endereco
        AC = MBR #AC recebe o valor pego na memória por MBR
        print("AC = ", AC)
    else: #se especificar qual o registrador
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2]) #busca o dado que esta no endereco
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

def executar_soma(memoria_volatil: list[str], instrucao: list[str]):
    global AC, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #se só tiver um elemento, soma-se com o AC
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        print("AC =", AC, "+", MBR, end=' ')
        AC += MBR
        print("=", AC)
    else:
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
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
    global AC, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #se só tiver um elemento, soma-se com o AC
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        print("AC =", AC, "+", MBR, end=' ')
        AC -= MBR
        print("=", AC)
    else:
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
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
    global MQ, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #se só tiver um elemento, soma-se com o AC
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        print("MQ =", MQ, "*", MBR, end=' ')
        MQ *= MBR
        print("=", MQ)
    else:
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
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
    global AC, R, MBR, GERAL_A, GERAL_B, GERAL_C
    if len(instrucao) == 2: #se só tiver um elemento, soma-se com o AC
        MBR = buscar_operando(memoria_volatil, instrucao[1])
        print(f"AC = {AC} / {MBR}", end=' ')
        R = AC % MBR
        AC //= MBR
        print(f"= {AC} (com resto R = {R})")
    else:
        registrador = instrucao[1].strip(',')
        MBR = buscar_operando(memoria_volatil, instrucao[2])
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

def executar_escrita(memoria_volatil: list[str], instrucao: list[str], arq: io.BytesIO):
    if len(instrucao) == 2: #tem apenas um dado a ser escrito na memoria.
        MBR = instrucao[1] #dado a ser escrito na memoria.
    print("Escrita feita!")

def executar_salto():
    print(AC)

def executar_salto_zero():
    print(AC)

def instrucoes(memoria_volatil: list[str], instrucao: str, arq: io.BytesIO) -> None:
    instrucao = instrucao.split(' ')
    IR = instrucao[0]
    print("Instrução atual -> IR: ", IR) #mostra qual instrução está sendo executada
    if IR == 'LOAD': #identifica a instrução
        executar_load(memoria_volatil, instrucao)
    elif IR == 'ADD':
        executar_soma(memoria_volatil, instrucao)
    elif IR == 'SUB':
        executar_subtracao(memoria_volatil, instrucao)
    elif IR == 'MULT':
        executar_multiplicacao(memoria_volatil, instrucao)
    elif IR == 'DIV':
        executar_divisao(memoria_volatil, instrucao)
    elif IR == 'STORE':
        executar_escrita(memoria_volatil, instrucao, arq)
    elif IR == 'JUMP':
        executar_salto()
    elif IR == '+JUMP':
        executar_salto_zero()

def le_instrucao(arq: io.TextIOWrapper, offset: int) -> tuple[str, int]:
    global PC, MAR
    '''pior que ela leu. fiquei em choque'''
    MAR = PC #endereço da instrução a ser executada -> apontada por PC
    print("Endereço da instrução atual -> MAR: ", MAR)
    arq.seek(offset, 0) #pula a memoria e as instruções já executadas
    instrucao = arq.readline().strip('\n') # le a próxima instrução
    PC = str(hex(int(PC, 16) + 1)).upper() #incrementa o pc (sim, joguei no google como somar está porra 1 a 1)
    return instrucao, arq.tell() #instrução lida, pc incrementado, offset da proxima instrucao (próxima linha)

def main():
    try:
        global PC, AC, IR
        arq = open('memoria.txt', 'r+')
        memoria_volatil, offset = contar_memoria(arq) #retorna os elementos da memória em forma de lista, pega o primeiro valor de PC (primeira linha pós memória) e o offset da próxima linha
        print("Endereço da próxima instrução -> PC: ", PC, "\n") #printa o primeiro endereco de PC
        for i in range(8):
            IR, offset = le_instrucao(arq, offset) #busca a proxima instrução (do endereço de PC) -> carrega em IR, incrementa PC e retorna o offset da próxima linha
            instrucoes(memoria_volatil, IR, arq) #usam os dados da "memoria_volatil" para executar a instrução de "IR".
            print("Endereço da próxima instrução -> PC: ", PC, "\n")

        arq.close()
    except:
        raise ValueError("Arquivo (memoria.txt) não encontrado.")

if __name__ == '__main__':
    main()



"""def buscar_operando(arq: io.TextIOWrapper, endereco: str) -> int:
    '''busca o endereco na memoria e retorna o dado que esta nele -> se for endereçamento direto. Caso seja imediato, retorna o dado'''
    arq.seek(0) #comeca a busca do inicio da memória
    palavra = arq.readline().strip('\n').split(' ') 
    while palavra[0] != endereco and palavra[0] != '0x0A':
        palavra = arq.readline().strip('\n').split(' ')
    if palavra[0] != '0x0A': 
        return int(palavra[1])
    else:
        print('Endereço não encontrado!')"""