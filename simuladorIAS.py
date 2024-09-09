'''
    Segundo Trabalho Prático
    Arquitetura e Organização de Computadores I / 12028 - 01
    Prof. Rodrigo Calvo

    Ana Paula Loureiro Crippa - RA 137304
    Maria Eduarda de Mello Policante - RA 134539
    Pâmela Camilo Chalegre - RA 134241
'''

import io

# ===== REGISTRADORES E VARIÁVEIS GLOBAIS =====

# Registradores de manipulam dados
MBR: int  # Buffer de memória
AC: int = 0  # Acumulador
MQ: int = 1  # Multiplicador
R: int  # Resto da divisao
C: int = 0  # Carry out (1: houve carry; 0: não houve)
Z: int = 0  # Resultado zero (1: resultado igual a zero; 0: resultado diferente)

# Registradores que armazenam partes da instrução
PC: str  # Contador de programa
MAR: str  # Endereço de memória
IR: str  # Instrução
GERAL_A: str = ''
GERAL_B: str = ''
GERAL_C: str = ''
GERAL_D: str = ''

# Variáveis auxiliares
OFFSET_ARQ: int  # Manipulação do arquivo
USO_ULA: int
BARRA_DADOS: int

# =============================================

# ============ FUNÇÕES AUXILIARES =============

def analisar_resultado(resultado: int) -> None:
    '''
    Analisa se o resultado de uma operação está dentro do limite estipulado de 10 bits. Como o máximo definido é 10 bits, o intervalo é de -1023 a 1024.
        :param int resultado: -> valor a ser analisado.
        :return None:
    '''
    global C, Z
    if -1023 < resultado < 1024: #se estiver dentro do limite
        C = 0 # não há carry
        if resultado == 0: # se o resultado for 0
            Z = 1
        else:
            Z = 0
    else: #se estiver fora do limite
        C = 1 # há carry
        Z = 0
    print("Análise do Resultado:\nZ =", Z, "| C =", C)

def atualizar_registrador(registrador: str, valor: int) -> None:
    '''
    Atualiza o registrador correto com seu novo valor, i.e., o valor resultante da instrução executada.
        :param str registrador: -> registrador a ser atualizado.
        :param int valor: -> novo valor do registrador.
        :return None:
    '''
    global GERAL_A, GERAL_B, GERAL_C, GERAL_D, MQ
    if registrador == 'A':
        GERAL_A = valor
    elif registrador == 'B':
        GERAL_B = valor
    elif registrador == 'C':
        GERAL_C = valor
    elif registrador == 'D':
        GERAL_D = valor
    elif registrador == 'MQ':
        MQ = valor

def buscar_endereco(memoria_volatil: list[str], endereco: str) -> int | str:
    '''
    Busca o endereco na memória e retorna o dado e sua posição na memória volátil se for endereçamento direto. Caso seja endereçamento imediato, retorna o proprio dado.
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param str endereco: -> endereço a ser buscado.
        :return int | str: -> dado ou operando.
    '''
    global MAR
    if endereco[:2] == 'M(':  # Endereçamento direto
        MAR = endereco[2:-1]  # MAR recebe o endereço a ser encontrado
        print("Busca do operando -> MAR:", MAR)
        i = int(MAR, 16)  # Transforma o endereço hexadecimal em INTEIRO
        palavra = memoria_volatil[i].strip('\n').split(sep=' ')  # Pega a palavra armazenada no endereço correto e divide entre endereço e dado
        
        if palavra[0] == MAR and len(palavra) == 2:  # Se existe um dado no endereço *referencia*
            return palavra[1] # dado
        elif palavra[0] == MAR and len(palavra) == 1: # Se não existe um dado no endereço *referencia*
            return '-1' # dado nulo
        else: # Se o endereço não foi encontrado
            raise ValueError("Endereço não encontrado")
    elif endereco[:2] == '0X': #se for enderecamento imediato -> o operando faz parte da instrucao
        return endereco # operando
    else:
        return endereco

def buscar_instrucao(arq: io.TextIOWrapper) -> tuple[str, int]:
    '''
    Busca a próxima instrução no endereço apontado por PC.
        :param io.TextIOWrapper arq: -> arquivo que contém as instruções.
        :return tuple[str, int]: -> instrução lida e offset da próxima instrução (linha seguinte).
    '''
    global PC, MAR
    MAR = PC  # Endereço da instrução a ser executada -> apontada por PC
    arq.seek(OFFSET_ARQ, 0)  # Pula a memória e as instruções já executadas
    instrucao = arq.readline().strip('\n')  # Lê a próxima instrução
    PC = str(hex(int(PC, 16) + 1)).upper()  # Incrementa o PC
    offset = arq.tell()
    return instrucao, offset

def buscar_referencia(memoria_volatil: list[str], parametro: str) -> int:
    '''
    Determina qual dado de registrador ou dado de memória a instrução precisa.
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param str parametro: -> registrador ou endereço a ser buscado.
        :return int: -> dado ou operando.
    '''
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
        print("MBR =", MBR)
        return int(MBR)

def carregar_memoria(arq: io.TextIOWrapper) -> tuple[list[str], int]:
    '''
    Carrega a memória volátil com os dados do arquivo.
        :param io.TextIOWrapper arq: arquivo que contém as instruções.
        :return tuple[list[str], int]: memória volátil de dados e a posição do início das instruções.
    '''
    global PC
    linha = arq.readline() # contador de linhas do arquivo
    memoria_volatil_dados: list[str] = []
    while linha != '\n': # a memória se separa das instrucoes
        memoria_volatil_dados.append(linha) # adiciona o dado lido à memoria de dados
        linha = arq.readline()
    offset = arq.tell()
    return memoria_volatil_dados, offset

# =============================================

# ============ FUNÇÕES PRINCIPAIS =============

def executar_LOAD(memoria_volatil: list[str], instrucao: list[str]) -> None: 
    '''
    Carrega um valor da memória no acumulador (AC) ou em outro registrador especificado: LOAD X | LOAD X, Y
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param list[str] instrucao: -> instrução a ser executada.
        :return None:
    '''
    global MBR, AC, MQ, GERAL_A, GERAL_B, GERAL_C, GERAL_D
    if len(instrucao) == 2:  # LOAD X : AC <- X
        MBR = int(buscar_endereco(memoria_volatil, instrucao[1]))  # Busca o dado que está no endereco
        print("MBR =", MBR)
        AC = MBR  # AC recebe o valor pego na memória por MBR
        print("AC =", AC)
    else:  # LOAD X, Y : X <- Y
        registrador = instrucao[1].strip(',')
        MBR = buscar_endereco(memoria_volatil, instrucao[2])  # Busca o dado que está no endereco
        print("MBR =", MBR)
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
    ''' 
    Move dados de um registrador para outro: MOV X | MOV X, Y
        :param list[str] instrucao: -> instrução a ser executada.
        :return None:
    '''
    global AC, MQ, GERAL_A, GERAL_B, GERAL_B, GERAL_C, GERAL_D
    registrador = instrucao[1].strip(',')  # Identificação do Registrador X
    if len(instrucao) == 2:  # MOV X : AC <- X (o valor de X vai para o AC)
        AC = int(buscar_referencia([], registrador))  # Não há busca por operandos na memória
        print(f"AC = {AC} (AC <- {registrador})")
    else:  # MOV X, Y : X <- Y (o valor de Y vai para X)
        fonte = instrucao[2]  # Valor 'fonte' será movido para o registrador X
        BARRA_DADOS = buscar_referencia([], fonte)
        atualizar_registrador(registrador, BARRA_DADOS)  # Atualiza o valor no Registrador X
        print(f"{registrador} = {BARRA_DADOS} ({registrador} <- {fonte})")
        
def executar_ADD(memoria_volatil: list[str], instrucao: list[str]) -> None:
    '''
    Soma um dado ao acumulador ou a outro registrador especificado: ADD X | ADD X, Y
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param list[str] instrucao: -> instrução a ser executada.
        :return None:
    '''
    global AC, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2:  # ADD X : AC <- AC + X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        print("AC =", AC, "+", BARRA_DADOS, end=' ')
        AC += BARRA_DADOS
        print("=", AC)
        analisar_resultado(AC)
    else:  # ADD X, Y : X <- X + Y
        USO_ULA = int(buscar_referencia(memoria_volatil, parametro))
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, instrucao[2]))
        print(f"Registrador {parametro} = {USO_ULA} + {BARRA_DADOS}", end=' ')
        USO_ULA += BARRA_DADOS
        print("=", USO_ULA)
        atualizar_registrador(parametro, USO_ULA)
        print("Memória volátil:", memoria_volatil)
        analisar_resultado(USO_ULA)

def executar_SUB(memoria_volatil: list[str], instrucao: list[str]) -> None:
    '''
    Subtrai um dado de AC ou outro registrador especificado: SUB X | SUB X, Y
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param list[str] instrucao: -> instrução a ser executada.
        :return None:
    '''
    global AC, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2:  # SUB X : AC <- AC - X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        print("AC =", AC, "-", BARRA_DADOS, end=' ')
        AC -= BARRA_DADOS
        print("=", AC)
        analisar_resultado(AC)
    else:  # SUB X, Y : X <- X - Y
        USO_ULA = int(buscar_referencia(memoria_volatil, parametro))
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, instrucao[2]))
        print(f"Registrador {parametro} = {USO_ULA} - {BARRA_DADOS}", end=' ')
        USO_ULA -= BARRA_DADOS
        atualizar_registrador(parametro, USO_ULA)
        print("=", USO_ULA)
        analisar_resultado(USO_ULA)

def executar_MULT(memoria_volatil: list[str], instrucao: list[str]) -> None:
    '''
    Multiplica um dado X pelo MQ ou outro registrador especificado: MULT X | MULT X, Y
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param list[str] instrucao: -> instrução a ser executada.
        :return None:
    '''
    global MQ, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2:  # MULT X : AC <- AC * X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        print("MQ =", MQ, "*", BARRA_DADOS, end=' ')
        MQ *= BARRA_DADOS
        print("=", MQ)
        analisar_resultado(MQ)
    else:  # MULT X, Y : X <- X * Y
        USO_ULA = int(buscar_referencia(memoria_volatil, parametro))
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, instrucao[2]))
        print(f"Registrador {parametro} = {USO_ULA} * {BARRA_DADOS}", end=' ')
        USO_ULA *= BARRA_DADOS
        atualizar_registrador(parametro, USO_ULA)
        print("=", USO_ULA)
        analisar_resultado(USO_ULA)

def executar_DIV(memoria_volatil: list[str], instrucao: list[str]) -> None:
    '''
    Divide o AC ou um registrador Y por um dado X: DIV X, Y; ou divide o AC pelo valor armazenado em X da memoria: DIV X
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param list[str] instrucao: -> instrução a ser executada.
        :return None:
    '''
    global AC, R, USO_ULA, BARRA_DADOS
    parametro = instrucao[1].strip(',')
    if len(instrucao) == 2:  # DIV X : AC <- AC // X
        BARRA_DADOS = int(buscar_referencia(memoria_volatil, parametro))
        if BARRA_DADOS == 0:
            raise ValueError("Divisão por 0.")
        else:
            print(f"AC = {AC} / {BARRA_DADOS}")
            R = AC % BARRA_DADOS
            AC //= BARRA_DADOS
            print(f"= {AC} (com resto R = {R})")
            analisar_resultado(AC)
    else:  # DIV X, Y : X <- X // Y
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
    '''
    Armazena um dado de um registrador na memória volátil. STOR X | STOR X, Y
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param list[str] instrucao: -> instrução a ser executada.
        :param io.TextIOWrapper arq: -> arquivo que contém as instruções.
        :return None:
    '''
    global MAR, AC
    
    local = instrucao[1].strip(',')  # Posição de memória que ocorrerá escrita
    if local[:2] == '0X':  # Posição está direta
        MAR = local
    else:  # Posição de escrita está armazenada em um registrador
        MAR = buscar_referencia([], local)  # MAR recebe a posição armazenada no registrador

    dado = buscar_endereco(memoria_volatil, MAR)  # Busca se o endereço MAR está na memoria_volatil
    posicao = int(MAR, 16)  # Transforma o endereço hexadecimal em inteiro
    if len(instrucao) == 2:  # STOR X : X <- AC
        print(memoria_volatil[posicao], "->", end=' ')  # Ir para a linha/posição do MAR
        if dado == '-1':  # Se não houver um dado escrito nela
            memoria_volatil[posicao] = memoria_volatil[posicao].strip('\n')
            memoria_volatil[posicao] += ' ' + str(AC) + '\n'
        else:  # Se já houver um dado, sobrescrever
            memoria_volatil[posicao] = memoria_volatil[posicao].split(' ')
            memoria_volatil[posicao][1] = str(AC) + '\n'
            memoria_volatil[posicao] = ' '.join(memoria_volatil[posicao])

    elif len(instrucao) == 3:  # STOR X, Y : X <- Y
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
    '''
    Executa um salto na execução sequencial das instruções: JUMP X : PC <- X
        :param io.TextIOWrapper arq: -> arquivo que contém as instruções.
        :param list[str] instrucao: -> instrução a ser executada.
        :param int offset_inst: -> offset do início das instruções.
        :return None:
    '''
    global PC, OFFSET_ARQ
    PC = instrucao[1]  # Pular para a rotina de instrução -> novo endereço
    print("Instrução de desvio -> PC:", PC)
    arq.seek(offset_inst)  # Vai pro começo das instruções
    OFFSET_ARQ = arq.tell()  # Armazena o offset novo
    volta = arq.readline().strip('\n')  # Primeiro endereco do PC -> 0X0A
    contar = volta
    while contar != PC:  # Se chegou ao endereco desejado
        OFFSET_ARQ = arq.tell()  # Atualiza o offset daquele endereço
        contar = str(hex(int(contar, 16) + 1)).upper()  # Incrementa o contador
        volta = arq.readline().strip('\n')
        # No fim, o offset do início da linha correspondente ao endereço de PC
        # É atualizado e levado para a leitura das proximas instruções

def executar_JUMP_zero(arq: io.TextIOWrapper, instrucao: list[str], offset_inst: int) -> None:
    '''
    Executa um salto na execução sequencial das instruções se o AC for MAIOR ou igual a 0: JUMP+ X : PC <- X (A >= 0)
        :param io.TextIOWrapper arq: -> arquivo que contém as instruções.
        :param list[str] instrucao: -> instrução a ser executada.
        :param int offset_inst: -> offset do início das instruções.
        :return None:
    '''
    global PC, AC, OFFSET_ARQ
    if AC >= 0:
        PC = instrucao[1]  # Pular para a rotina de instrução -> novo endereço
        print("Instrução de desvio -> PC:", PC)
        arq.seek(offset_inst)  # Vai pro começo das instruções
        OFFSET_ARQ = arq.tell()  # Armazena o offset novo
        volta = arq.readline().strip('\n')  # Primeiro endereco do PC -> 0X0A
        contar = volta
        while contar != PC:  # Se chegou ao endereco desejado
            OFFSET_ARQ = arq.tell()  # Atualiza o offset daquele endereço
            contar = str(hex(int(contar, 16) + 1)).upper()  # Incrementa o contador
            volta = arq.readline().strip('\n')
        # No fim, o offset do início da linha correspondente ao endereço de PC
        # É atualizado e levado para a leitura das proximas instruções
    else:
        print(f"Instrução não executada! Condição não respeitada! (AC = {AC})")

def executar_LSH() -> None:
    '''
    Desloca os bits do registrador AC para a esquerda. Equivale a multiplicar o valor em AC por 2.
        :return None:
    '''
    global AC
    print("AC =", AC)
    AC = AC << 1  # Desloca o conteúdo de AC uma posição à esquerda
    print(f"AC = {AC} -> AC * 2 (<< LSH)")

def executar_RSH() -> None:
    '''
    Desloca os bits do registrador AC para a direita. Equivale a dividir o valor em AC por 2.
        :return None:
    '''
    global AC
    print("AC =", AC)
    AC = AC >> 1  # Desloca o conteúdo de AC uma posição à direita
    print(f"AC = {AC} -> AC / 2 (>> RSH)")

def executar_instrucao(memoria_volatil: list[str], instrucao: str, arq: io.TextIOWrapper, offset_inst: int) -> None:
    '''
    Executa a instrução atual, e identifica qual instrução está sendo executada.
        :param list[str] memoria_volatil: -> contém os dados e endereços.
        :param str instrucao: -> instrução a ser executada.
        :param io.TextIOWrapper arq: -> arquivo que contém as instruções.
        :param int offset_inst: -> offset do início das instruções.
        :return None:
    '''
    global IR
    instrucao = instrucao.split(' ')
    IR = instrucao[0]
    print("Instrução atual -> IR:", IR)  # Mostra qual instrução está sendo executada
    if IR == 'LOAD':  # Identifica a instrução
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

# =============================================

# ============ FUNÇÃO DE EXECUÇÃO =============

def main():
    try:
        global PC, IR, OFFSET_ARQ, MAR, GERAL_D
        arqOp = input("\nDigite o nome (com extensão .txt) do arquivo de memória a ser executado: ")  # Define o arquivo de operações
        arq = open(arqOp, 'r+')
        memoria_volatil_dados, OFFSET_ARQ = carregar_memoria(arq)  # Carrega os elementos da memória em uma lista e pega o primeiro valor de PC (primeira linha pós memória) e o offset da próxima linha
        comeco = OFFSET_ARQ  # Guarda o primeiro offset das instruções

        PC = arq.readline().strip('\n')  # O primeiro endereco do PC é a primeira linha pós-memória
        OFFSET_ARQ = arq.tell()  # Offset após ler PC
        print("Endereço da próxima instrução -> PC =", PC, "\n")
        MBR, OFFSET_ARQ = buscar_instrucao(arq)  # Busca a proxima instrução (endereço de PC) -> carrega em MBR, incrementa PC e retorna o offset da próxima linha
        while MBR != '':
            print('Busca da instrução -> Endereço -> MAR =', MAR)
            print("MBR =", MBR)
            executar_instrucao(memoria_volatil_dados, MBR, arq, comeco) # Usa os dados da "memoria_volatil" para executar a instrução de "MBR"
            print("Endereço da próxima instrução -> PC =", PC, "\n")
            MBR, OFFSET_ARQ = buscar_instrucao(arq)  # Busca a proxima instrução (endereço de PC) -> carrega em MBR, incrementa PC e retorna o offset da próxima linha

        arq.seek(comeco)
        memoria_volatil_instrucoes = arq.readlines()  # Guarda todas as instruções do arquivo em uma memoria volátil
        arq.seek(0)
        for i in range(len(memoria_volatil_dados)):  # Escreve a memória_volátil atualizada na memória principal
            arq.write(memoria_volatil_dados[i])
        arq.write('\n')
        for j in range(len(memoria_volatil_instrucoes)):  # Reescreve as instruções na memória
            arq.write(memoria_volatil_instrucoes[j])

        arq.close()

    except FileNotFoundError:
        print(f'\nArquivo "{arq.name}" não encontrado.\n')

if __name__ == '__main__':
    main()

# =============================================
