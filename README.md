# Simulador do Computador IAS

Este projeto é um simulador do comportamento dos registradores de um processador, inspirado na arquitetura do computador IAS. O simulador executa uma sequência de comandos de linguagem de máquina, armazenando dados em registradores para realizar operações básicas como adição, subtração, multiplicação, divisão, transferência de dados e desvio de fluxo.

O computador IAS foi o primeiro computador eletrônico, desenvolvido pelo Instituto de Estudos Avançados de Princeton (IAS). Ele era uma máquina binária, com uma palavra de 40 bits de comprimento, na qual era possível armazenar duas instruções de 20 bits. O IAS foi criado para diminuir o tempo necessário para executar instruções. Além disso, ele permitiu armazenar instruções e dados na mesma memória.

## Descrição

O objetivo deste projeto foi desenvolver um programa que simula o comportamento dos registradores de um processador durante a execução de um ciclo de instrução. Todas as instruções e dados necessários para a simulação são armazenados em memória RAM e o conteúdo dos registradores é exibido após cada instrução.

O simulador executa o algoritmo de ordenação por Seleção (Selection Sort) e o algoritmo do cálculo de média, o qual foi escolhido pelo grupo. As instruções para cada algoritmo são fornecidas através de um arquivo texto, onde os dados e a sequência de comandos são especificados.

## Como executar?

Para executar o simulador do computador IAS, siga os passos abaixo:

1. Execute o script principal do simulador: python registradoresORDEM.py

2. O programa solicitará o nome do arquivo de memória a ser executado. Insira o nome do arquivo, incluindo a extensão .txt.

3. Dessa forma, o simulador processará as instruções no arquivo e exibirá na tela o conteúdo dos registradores e as micro-operações realizadas em cada etapa.

## Integrantes

| Nome | RA |
|-----|-----|
| Ana Paula Loureiro Crippa | 137304 |
| Maria Eduarda de Mello Policante | 134539 |
| Pâmela Camilo Chalegre | 134241 |

## Estrutura do código

O simulador é composto por uma série de funções que representam as operações realizadas pelo computador IAS.

Os registradores são memórias voláteis, os quais foram implementados como variáveis globais, e são utilizados para armazenar dados e resultados intermediários durante a simulação.

escrever maisssss ...??

## Registradores

### Presentes na Unidade de Controle (UC)

- PC (*Program Counter*)
	> Armazena um valor que representa o endereço de memória, o qual possui a próxima instrução a ser executada.
	> No início, quando o programa é executado, o conteúdo deste registrador é zerado.

- MAR (*Memory Address Register*) 
	> Armazena um valor que representa o endereço de memória da palavra que está sendo acessada.
	> Este endereço é lido pela memória durante operações de leitura ou escrita de dados.

- IR (*Instruction Register*)
	> Armazena a instrução que está sendo executada no momento.
	> A Unidade de Controle lê e interpreta os bits desse registrador, de modo a enviar sinais de controle para o restante do computador, a fim de coordenar a execução da instrução armazenada.

- IBR (*Instruction Buffer*)
	> Armazena temporariamente a instrução mais a direita da palavra.
	> Apesar de este registrador estar presente no computador IAS, devido às especificações propostas pelo professor, decidimos por não implementar o IBR em nosso trabalho.

### Presentes na Unidade Lógica e Aritmética (ULA)

- MBR (*Memory Buffer Register*)
	> Armazena temporariamente dados lidos da memória ou dados que ainda serão escritos na memória.

- AC (*Accumulator*)
	> Armazena temporariamente operandos e resultados de operações lógicas e aritméticas.
	> Serve como registrador padrão, isto é, caso não seja explicitado um endereço para as operações LOAD, STOR, ADD, SUB, LSH e RSH, é o registrador AC que armazenará o operando ou o resultado.

- MQ (*Multiplier Quotient*)
	> Armazena temporariamente operandos e resultados de operações aritméticas.
	> Serve como registrador padrão, isto é, caso não seja explicitado um endereço para as operações MUL e DIV, é o registrador MQ que armazenará o operando ou o resultado.

## Funções

### Principais

executar_LOAD: Carrega um valor da memória no acumulador ou em outro registrador especificado.

executar_ADD: Soma um dado ao acumulador ou a outro registrador especificado.

executar_SUB: Subtrai um dado do acumulador ou de outro registrador especificado.

executar_MULT: Multiplica um dado pelo MQ ou outro registrador especificado.

executar_DIV: Divide o acumulador ou um registrador específico por um dado.

executar_STOR: Armazena um dado de um registrador na memória volátil. Pode armazenar o valor do AC ou de outro registrador em um endereço de memória especificado.

executar_JUMP: Executa um salto na execução das instruções, alterando o PC para o endereço especificado.

executar_JUMP_zero: Executa um salto na execução das instruções se o valor do acumulador for maior ou igual a zero.

executar_LSH: Desloca os bits do registrador AC para a esquerda (LSH - Left Shift), equivalente a multiplicar o valor em AC por 2.

executar_RSH: Desloca os bits do registrador AC para a direita (RSH - Right Shift), equivalente a dividir o valor em AC por 2.

### Auxiliares

analisar_resultado: Verifica se o resultado da operação está dentro dos limites e ajusta os registradores de carry (C) e zero (Z) conforme necessário.

carregar_memoria: Lê o arquivo de memória e carrega os dados na memória volátil. Retorna os dados e o offset onde começam as instruções reais.

buscar_endereco: Busca o endereço na memória volátil e retorna o dado correspondente ou o próprio dado se for endereçamento imediato.

buscar_referencia: Identifica e retorna o dado necessário da memória ou do registrador conforme a instrução.

atualizar_registrador: Atualiza o registrador correto com o novo valor resultante da instrução executada.

## Referências

BORIN, Edson; AULER, Rafael. Programando o computador IAS. UNICAMP, 2012. Disponível em: https://www.ic.unicamp.br/~edson/disciplinas/mc404/2012-1s/anexos/programando_o_IAS.pdf. Acesso em: 14 ago. 2024.

colocar os materiais do calvo aqui tb
