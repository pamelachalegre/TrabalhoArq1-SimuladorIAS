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
C: int = 0 # Carry out (1: houve carry; 0: não houve carry) -> MAX: 10 BITS -> 1024 e -1023
Z: int = 0 # Resultado zero (0: resultado diferente de 0; 1: resultado igual a zero)
#registradores que armazenam partes da instrucao:
PC: str
IR: str
MAR: str
MBR: int
GERAL_A: str = ''
GERAL_B: str = ''
GERAL_C: str = ''
GERAL_D: str = ''
OFFSET_ARQ: int #variavel para manipulação do arquivo
USO_ULA: int
BARRA_DADOS: int

def analisar_resultado(resultado: int):
    global C, Z
    if -1023 < resultado < 1024: #se estiver dentro do limite estipulado -> 10 bits
        C = 0 # não há carry
        if resultado == 0: #se o resultado for 0:
            Z = 1 #Z passa para 0
        else:
            Z = 0
    else: #se estiver fora dos limites de 10 bits
        C = 1 #há carry
        Z = 0 #e o resultado não é zero
    print("Análise do Resultado : Z =", Z, "| C =", C)

def carregar_memoria(arq: io.TextIOWrapper) -> tuple[list[str], int]:
    global PC
    '''conta quantas linhas tem o arquivo'''
    linha = arq.readline()
    memoria_volatil_dados: list[str] = []
    while linha != '\n': #a memória se separa das instrucoes
        memoria_volatil_dados.append(linha) #adiciona o dado lido a memoria de dados
        linha = arq.readline()
    return memoria_volatil_dados, arq.tell() #offset -> onde vão começar as instruções reais

def buscar_endereco(memoria_volatil: list[str], referencia: str) -> int:
    '''Busca o endereco "referencia" na memoria e retorna o dado e sua posição na memória volátil se for endereçamento direto. 
    Caso seja endereçamento imediato, retorna o proprio dado.'''
    global MAR
    if referencia[:2] == 'M(': # Se for um endereco -> endereçamento direto
        MAR = referencia[2:-1] #o MAR recebe o endereço a ser encontrado
        print("Busca do operando -> MAR:", MAR)
        i = int(MAR, 16) #transforma o endereço hexadecimal em INTEIRO  -> O endereço inicial é o 0X00 que corresponde ao índice 0 da memória volátil.
        palavra = memoria_volatil[i].strip('\n').split(sep=' ') #pega a palavra aramazenada no endereço correto e divide (endereco e dado).
        
        if palavra[0] == MAR and len(palavra) == 2: # Se existe um dado no endereço *referencia*
            return palavra[1] # dado
        elif palavra[0] == MAR and len(palavra) == 1: # Se não existe um dado no endereço *referencia*
            return '-1' # dado nulo
        else: # Se o endereço não foi encontrado
            raise ValueError("Endereço não encontrado")
    elif referencia[:2] == '0X': #se for enderecamento imediato -> o operando faz parte da instrucao
        return referencia # operando
    else:
        return referencia

def buscar_referencia(memoria_volatil: list[str], parametro: str) -> str | int:
    '''Determina qual dado de registrador ou dado de memória a instrução precisa e o retorna'''
    global MQ, GERAL_A, GERAL_B, GERAL_C, GERAL_D, MBR
    if parametro == 'A':
        return GERAL_A
    elif parametro == 'B':
        return GERAL_B
    elif parametro == 'C':
        return GERAL_C
    elif parametro == 'D':
        return GERAL_D
    elif parametro == 'MQ':
        return MQ
    else:
        MBR = buscar_endereco(memoria_volatil, parametro)
        print("MBR:", MBR)
        return int(MBR)

def atualizar_registrador(parametro: str, valor: int):
    '''Atualiza o registrador correto com seu novo valor (resultante da instrução executada).'''
    global MQ, GERAL_A, GERAL_B, GERAL_C, GERAL_D
    if parametro == 'A':
        GERAL_A = valor
    elif parametro == 'B':
        GERAL_B = valor
    elif parametro == 'C':
        GERAL_C = valor
    elif parametro == 'D':
        GERAL_D = valor
    elif parametro == 'MQ':
        MQ = valor

def executar_LOAD(memoria_volatil: list[str], instrucao: list[str]) -> None: 
    ''' LOAD X | LOAD X, Y
    Carrega um valor da memória no acumulador (AC) ou em outro registrador especificado.'''
    global MBR, AC, MQ, GERAL_A, GERAL_B, GERAL_C, GERAL_D
    if len(instrucao) == 2: #LOAD X : AC <- X
        MBR = int(buscar_endereco(memoria_volatil, instrucao[1])) #busca o dado que esta no endereco
        print("MBR:", MBR)
        AC = MBR #AC recebe o valor pego na memória por MBR
        print("AC =", AC)
    else: #LOAD X, Y : X <- Y
        registrador = instrucao[1].strip(',')
        MBR = buscar_endereco(memoria_volatil, instrucao[2]) #busca o dado que esta no endereco
        print("MBR:", MBR)
        if registrador == 'MQ':
            MQ = int(MBR)
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
        elif registrador == 'D':
            GERAL_D = MBR
            print("Registrador D =", GERAL_D)

def executar_MOV(instrucao: list[str]) -> None:
    ''' MOV X | MOV X, Y 
    Move dados de um registrador para outro.'''
    global AC, MQ, GERAL_A, GERAL_B, GERAL_B, GERAL_C, GERAL_D
    registrador = instrucao[1].strip(',') #Registrador X (elemento obrigatório)
    if len(instrucao) == 2: #MOV X : AC <- X (o valor de X vai para o AC)
        AC = int(buscar_referencia([], registrador)) #não há busca por operandos na memória
        print(f"AC = {AC} (AC <- {registrador})")
    else: #MOV X, Y : X <- Y (o valor de Y vai para X)
        fonte = instrucao[2] #o valor da FONTE será movido para o registrador X
        BARRA_DADOS = buscar_referencia([], fonte)
        atualizar_registrador(registrador, BARRA_DADOS) #Coloca o valor posto em "barra_dados" no registrador X correto
        print(f"{registrador} = {BARRA_DADOS} ({registrador} <- {fonte})")
        
def executar_ADD(memoria_volatil: list[str], instrucao: list[str]):
    ''' ADD X | ADD X, Y
    Soma um dado ao acumulador ou a outro registrador especificado.'''
    global AC, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2: #ADD X : AC <- AC + X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        print("AC =", AC, "+", BARRA_DADOS, end=' ')
        AC += BARRA_DADOS
        print("=", AC)
        analisar_resultado(AC)
    else: #ADD X, Y : X <- X + Y
        USO_ULA = int(buscar_referencia(memoria_volatil, parametro))
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, instrucao[2]))
        print(f"Registrador {parametro} = {USO_ULA} + {BARRA_DADOS}", end=' ')
        USO_ULA += BARRA_DADOS
        print("=", USO_ULA)
        atualizar_registrador(parametro, USO_ULA)
        print("Memória volátil:", memoria_volatil)
        analisar_resultado(USO_ULA)

def executar_SUB(memoria_volatil: list[str], instrucao: list[str]):
    ''' SUB X | SUB X, Y 
    Subtrai um dado de AC ou outro registrador especificado.'''
    global AC, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2: #SUB X : AC <- AC - X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        print("AC =", AC, "-", BARRA_DADOS, end=' ')
        AC -= BARRA_DADOS
        print("=", AC)
        analisar_resultado(AC)
    else: # SUB X, Y : X <- X - Y
        USO_ULA = int(buscar_referencia(memoria_volatil, parametro))
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, instrucao[2]))
        print(f"Registrador {parametro} = {USO_ULA} - {BARRA_DADOS}", end=' ')
        USO_ULA -= BARRA_DADOS
        atualizar_registrador(parametro, USO_ULA)
        print("=", USO_ULA)
        analisar_resultado(USO_ULA)

def executar_MULT(memoria_volatil: list[str], instrucao: list[str]):
    ''' MULT X | MULT X, Y
    Multiplica um dado X pelo MQ ou outro registrador especificado.'''
    global MQ, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2: #MULT X : AC <- AC * X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        print("MQ =", MQ, "*", BARRA_DADOS, end=' ')
        MQ *= BARRA_DADOS
        print("=", MQ)
        analisar_resultado(MQ)
    else: # MULT X, Y : X <- X * Y
        USO_ULA = int(buscar_referencia(memoria_volatil, parametro))
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, instrucao[2]))
        print(f"Registrador {parametro} = {USO_ULA} * {BARRA_DADOS}", end=' ')
        USO_ULA *= BARRA_DADOS
        atualizar_registrador(parametro, USO_ULA)
        print("=", USO_ULA)
        analisar_resultado(USO_ULA)

def executar_DIV(memoria_volatil: list[str], instrucao: list[str]):
    ''' DIV X | DIV X, Y
    Divide o AC ou um registrador específico (Y) por um dado X
    Divide o valor em AC pelo valor armazenado no endereco X da memoria.
    '''
    global AC, R, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2: # DIV X : AC <- AC // X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        if BARRA_DADOS == 0:
            raise ValueError("Divisão por 0.")
        else:
            print(f"AC = {AC} / {BARRA_DADOS}")
            R = AC % BARRA_DADOS
            AC //= BARRA_DADOS
            print(f"= {AC} (com resto R = {R})")
            analisar_resultado(AC)
    else: # DIV X, Y : X <- X // Y
        USO_ULA = int(buscar_referencia(memoria_volatil, parametro))
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, instrucao[2]))
        if BARRA_DADOS == 0:
            raise ValueError("Divisão por 0.")
        else:
            print(f"{parametro} = {USO_ULA} / {BARRA_DADOS}")
            R = USO_ULA % BARRA_DADOS
            USO_ULA //= BARRA_DADOS
            print(f"= {USO_ULA} (com resto R = {R})")
            atualizar_registrador(parametro, USO_ULA)
            analisar_resultado(USO_ULA)

def executar_STOR(memoria_volatil: list[str], instrucao: list[str], arq: io.TextIOWrapper) -> None:
    ''' Armazena um dado de um registrador na memória volátil.
    STOR 0X05      -> len(instrucao) = 2 -> escreve o AC na posição 0X05 : 0X05 <- AC
    STOR 0X01, A   -> len(instrucao) = 3 -> escreve A na posição 0X01 : 0X01 <- A
    '''
    global MAR, AC
    
    local = instrucao[1].strip(',') # posição de memória que é pra escrever -> 0X
    if local[:2] == '0X': # se for a posição diretamente
        MAR = local #MAR recebe a posição
    else: # se a posição de escrita está armazenada em um registrador
        MAR = buscar_referencia([], local) # MAR recebe a posição armazenada nele

    dado = buscar_endereco(memoria_volatil, MAR) # busca se o endereço MAR está na memoria_volatil
    posicao = int(MAR, 16) #transforma o endereço hexadecimal em INTEIRO.
    if len(instrucao) == 2: # STOR X : X <- AC
        # ir para a linha/posição do MAR
        print(memoria_volatil[posicao], "->", end=' ')
        if dado == '-1': # se não houver um dado escrito nela
            memoria_volatil[posicao] = memoria_volatil[posicao].strip('\n')
            memoria_volatil[posicao] += ' ' + str(AC) + '\n'
        else: #se já houver um dado, sobrescreve
            memoria_volatil[posicao] = memoria_volatil[posicao].split(' ')
            memoria_volatil[posicao][1] = str(AC) + '\n'
            memoria_volatil[posicao] = ' '.join(memoria_volatil[posicao])

    elif len(instrucao) == 3: # STOR X, Y : X <- Y
        registrador = buscar_referencia([], instrucao[2])
        if dado == '-1':
            memoria_volatil[posicao] = memoria_volatil[posicao].strip('\n')
            memoria_volatil[posicao] += ' ' + str(registrador) + '\n'
        else:
            memoria_volatil[posicao] = memoria_volatil[posicao].split(' ')
            memoria_volatil[posicao][1] = str(registrador) + '\n'
            memoria_volatil[posicao] = ' '.join(memoria_volatil[posicao])
        
    print(memoria_volatil[posicao], "\nEscrita feita!")

def executar_JUMP(arq: io.TextIOWrapper, instrucao: list[str], offset_inst: int) -> None:
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

def executar_JUMP_zero(arq: io.TextIOWrapper, instrucao: list[str], offset_inst: int) -> None:
    ''' JUMP+ X : PC <- X (A >= 0)
    Executa um salto na execução sequencial das instruções se o AC for MAIOR ou igual a 0.'''
    global PC, AC, OFFSET_ARQ
    if AC >= 0:
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

def executar_LSH() -> None:
    '''
    Desloca os bits do registrador AC para a esquerda.
    Equivale `a multiplicar o valor em AC por 2
    '''
    global AC
    print("AC =", AC)
    AC = AC << 1 #desloca o conteúdo de AC uma posição à esquerda
    print(f"AC = {AC} -> AC * 2 (<< LSH)")

def executar_RSH() -> None:
    '''
    Desloca os bits do registrador AC para a direita.
    Equivale `a dividir o valor em AC por 2
    '''
    global AC
    print("AC =", AC)
    AC = AC >> 1 #desloca o conteúdo de AC uma posição à direita
    print(f"AC = {AC} -> AC / 2 (>> RSH)")

def executar_instrucao(memoria_volatil: list[str], instrucao: str, arq: io.TextIOWrapper, offset_inst: int) -> None:
    global IR
    instrucao = instrucao.split(' ')
    IR = instrucao[0]
    print("Instrução atual -> IR:", IR) #mostra qual instrução está sendo executada
    if IR == 'LOAD': #identifica a instrução
        executar_LOAD(memoria_volatil, instrucao)
    elif IR == 'MOV':
        executar_MOV(instrucao)
    elif IR == 'ADD':
        executar_ADD(memoria_volatil, instrucao)
    elif IR == 'SUB':
        executar_SUB(memoria_volatil, instrucao)
    elif IR == 'MULT':
        executar_MULT(memoria_volatil, instrucao)
    elif IR == 'DIV':
        executar_DIV(memoria_volatil, instrucao)
    elif IR == 'JUMP':
        executar_JUMP(arq, instrucao, offset_inst)
    elif IR == 'JUMP+':
        executar_JUMP_zero(arq, instrucao, offset_inst)
    elif IR == 'STOR':
        executar_STOR(memoria_volatil, instrucao, arq)
    elif IR == 'LSH':
        executar_LSH()
    elif IR == 'RSH':
        executar_RSH()
    else:
        print("Instrução inválida! Executando a próxima instruçao:")

def buscar_instrucao(arq: io.TextIOWrapper) -> tuple[str, int]:
    global PC, MAR
    '''Busca a próxima instrução no endereço apontado por PC.'''
    MAR = PC #endereço da instrução a ser executada -> apontada por PC
    arq.seek(OFFSET_ARQ, 0) #pula a memoria e as instruções já executadas
    instrucao = arq.readline().strip('\n') # le a próxima instrução
    PC = str(hex(int(PC, 16) + 1)).upper() #incrementa o PC
    return instrucao, arq.tell() #instrução lida, offset da proxima instrucao (próxima linha)

def main():
    try:
        global PC, IR, OFFSET_ARQ, MAR, GERAL_D
        arq = input("\nDigite o nome (com extensão .txt) do arquivo de memória a ser executado: ") #pergunta qual o arquivo de operações
        arq = open(arq, 'r+') #abre o arquivo
        memoria_volatil_dados, OFFSET_ARQ = carregar_memoria(arq) #retorna os elementos da memória em forma de lista, pega o primeiro valor de PC (primeira linha pós memória) e o offset da próxima linha
        comeco = OFFSET_ARQ #variável para o primeiro offset das instruções

        PC = arq.readline().strip('\n') #primeiro endereco do PC -> primeira linha pós-memória (tira o \n da quebra)
        OFFSET_ARQ = arq.tell() #offset após ler o PC
        print("Endereço da próxima instrução -> PC:", PC, "\n") #printa o primeiro endereco de PC
        MBR, OFFSET_ARQ = buscar_instrucao(arq) #busca a proxima instrução (do endereço de PC) -> carrega em MBR, incrementa PC e retorna o offset da próxima linha
        while MBR != '':
            print("Busca da instrução -> Endereço -> MAR:", MAR)
            print("MBR:", MBR)
            executar_instrucao(memoria_volatil_dados, MBR, arq, comeco) #usam os dados da "memoria_volatil" para executar a instrução de "MBR".
            print("GERAL D ============= ", GERAL_D)
            print("Endereço da próxima instrução -> PC: ", PC, "\n")
            MBR, OFFSET_ARQ = buscar_instrucao(arq) #busca a proxima instrução (do endereço de PC) -> carrega em MBR, incrementa PC e retorna o offset da próxima linha

        arq.seek(comeco)
        memoria_volatil_instrucoes = arq.readlines() #pega todas as instruções do arquivo e guarda em uma memoria volátil
        arq.seek(0)
        for i in range(len(memoria_volatil_dados)):
            arq.write(memoria_volatil_dados[i]) # escreve a memória_volátil atualizada na memória principal
        arq.write('\n')
        for j in range(len(memoria_volatil_instrucoes)): # reescreve as instruções na memória
            arq.write(memoria_volatil_instrucoes[j])

        arq.close()

    except FileNotFoundError:
        print(f"\nArquivo '{arq}' não encontrado.\n")

if __name__ == '__main__':
    main()
