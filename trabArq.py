'''
TRABALHO ARQUITETURA E ORGANIZAÇÃO DE COMPUTADORES 1
ALUNA: Ana Paula Loureiro Crippa - RA 137304
ALUNA: Maria Eduarda de Mello Policante - RA 134539
ALUNA: Pâmela Camilo Chalegre - RA 134241
'''

import io

#registradores de manipulam dados:
AC: int = 0 #acumulador
MQ: int #multiplicador
R: int #resto da divisao
C: int #carry (1, 2)
Z: int #natureza do resultado (-1, 0, 1)
#registradores que armazenam partes da instrucao:
PC: str
IR: str
MAR: str
MBR: str
USO_GERAL1: str
USO_GERAL2: str

def achar_endereco(arq: io.TextIOWrapper, endereco: str) -> int:
    '''busca o endereco na memoria e retorna o dado que esta nele'''
    arq.seek(0) #comeca a busca do inicio da memória
    palavra = arq.readline().strip('\n').split(' ') 
    while palavra[0] != endereco and palavra[0] != '0x0A':
        palavra = arq.readline().strip('\n').split(' ')
    if palavra[0] != '0x0A': 
        return int(palavra[1])
    else:
        print('Endereço não encontrado!')
    
def contar_memoria(arq: io.TextIOWrapper) -> tuple[int, int]:
    global PC
    '''conta quantas linhas tem o arquivo'''
    linha = arq.readline()
    n_linhas = 1
    while linha != '\n':
        linha = arq.readline()
        n_linhas += 1
    PC = arq.readline().strip('\n') #primeiro endereco do PC -> primeira linha pós-memória (tira o \n da quebra)
    return n_linhas, arq.tell() #offset -> onde vão começar as instruções reais
        
def executar_load(arq: io.TextIOWrapper, endereco: str, registrador: str) -> None: 
    '''EM TESTE!!!! carrega o valor de um endereço de memória no acumulador (AC) ou em outro registrador especificado'''
    global AC, MQ, USO_GERAL1
    valor = achar_endereco(arq, endereco) #busca o valor que esta no endereco
    if registrador == 'AC':
        AC = valor
        print("AC = ", AC)
    else:
        if registrador == 'MQ':
            MQ = valor
            print("MQ = ", MQ)
        else:
            USO_GERAL1 = valor
            print("Registrador = ", USO_GERAL1)

def executar_soma(arq: io.TextIOWrapper, instrucao: list[str]):
    global AC
    if len(instrucao) == 2: #se só tiver um elemento, soma-se com o AC
        dado = achar_endereco(arq, instrucao[1])
        print("AC =", AC, "+", dado, end=' ')
        AC += dado
        print("=", AC)
    else:
        print()

def executar_multiplicacao():
    global MQ
    print(MQ)

def instrucoes(arq: io.TextIOWrapper, instrucao: str) -> None:
    instrucao = instrucao.split(' ')
    if instrucao[0] == 'LOAD':
        executar_load(arq, instrucao)
    elif instrucao[0] == 'ADD':
        executar_soma(arq, instrucao)
    elif instrucao[0] == 'MULT':
        executar_multiplicacao(arq, instrucao)

def le_instrucao(arq: io.TextIOWrapper, offset: int) -> tuple[str, int]:
    global PC
    '''pior que ela leu. fiquei em choque'''
    print("Endereço da próxima instrução -> PC: ", PC) # o endereco que estamos buscando
    arq.seek(offset, 0) #pula a memoria e as instruções já executadas
    instrucao = arq.readline().strip('\n') # le a próxima instrução
    PC = str(hex(int(PC, 16) + 1)).upper() #incrementa o pc (sim, joguei no google como somar está porra 1 a 1)
    return instrucao, arq.tell() #instrução lida, pc incrementado, offset da proxima instrucao (próxima linha)

def main():
    try:
        global PC, IR
        arq = open('memoria.txt', 'r+')
        tam_memoria, offset = contar_memoria(arq) #conta quantas linhas a parte da memória tem, pega o primeiro valor de PC (primeira linha pós memória) e o offset da próxima linha
        for i in range(2):
            IR, offset = le_instrucao(arq, offset) #busca a proxima instrução (do endereço de PC) -> carrega em IR, incrementa PC e retorna o offset da próxima linha
            print("Instrução -> IR: ", IR) #ultima insrução buscada -> a do endereço do PC PRÉ-incremento
            instrucoes(arq, IR)

        arq.close()
    except:
        raise ValueError("Arquivo (memoria.txt) não encontrado.")

if __name__ == '__main__':
    main()