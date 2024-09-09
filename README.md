# Simulador do Computador IAS

Este projeto é um simulador do comportamento dos registradores de um processador, inspirado na arquitetura do computador IAS. O simulador executa uma sequência de comandos de linguagem de máquina, armazenando dados em registradores para realizar operações básicas como adição, subtração, multiplicação, divisão, transferência de dados e desvio de fluxo.

O computador IAS foi o primeiro computador eletrônico, desenvolvido pelo Instituto de Estudos Avançados de Princeton (IAS). Ele era uma máquina binária, com uma palavra de 40 bits de comprimento, na qual era possível armazenar duas instruções de 20 bits. O IAS foi criado para diminuir o tempo necessário para executar instruções. Além disso, ele permitiu armazenar instruções e dados na mesma memória.

## Descrição

O objetivo deste projeto foi desenvolver um programa que simula o comportamento dos registradores de um processador durante a execução de um ciclo de instrução. Todas as instruções e dados necessários para a simulação são armazenados em memória RAM e o conteúdo dos registradores é exibido após cada instrução.

O simulador executa o algoritmo de ordenação por Seleção (Selection Sort) e o algoritmo do cálculo de média, o qual foi escolhido pelo grupo. As instruções para cada algoritmo são fornecidas através de um arquivo texto, onde os dados e a sequência de comandos são especificados.

## Integrantes

| Nome | RA |
|--|--|
| Ana Paula Loureiro Crippa | 137304 |
| Maria Eduarda de Mello Policante | 134539 |
| Pâmela Camilo Chalegre | 134241 |

## Como executar?

Para executar o simulador do computador IAS, siga os passos abaixo:

1. Descompacte o arquivo:
	```
	cpu_ra137304_ra134539_ra134241.zip
	```
2. Execute o script principal do simulador: 
	```
	python simuladorIAS.py
	```
3. O programa solicitará o nome do arquivo de memória a ser executado. Insira o nome do arquivo, incluindo a extensão .txt. Por exemplo:
	```
	media.txt
	selectionsort.txt
	```
4. Dessa forma, o simulador processará as instruções no arquivo e exibirá na tela o conteúdo dos registradores e as micro-operações realizadas em cada etapa.

## Estrutura do código

Os registradores são memórias voláteis e de tamanho limitado, são utilizados para armazenar dados e resultados intermediários durante a simulação. Como são pequenas unidades de armazenamento dentro do processador que guardam dados temporários durante a execução de instruções, escolhemos representar todos os registradores como variáveis.

O simulador é composto por uma série de funções que representam as operações realizadas pelo computador IAS.

## Registradores

### Presentes na Unidade Lógica e Aritmética (ULA)

- MBR (*Memory Buffer Register*)
	> Armazena temporariamente dados lidos da memória ou dados que ainda serão escritos na memória.

- AC (*Accumulator*)
	> Armazena temporariamente operandos e resultados de operações lógicas e aritméticas.
	> Serve como registrador padrão, isto é, caso não seja explicitado um endereço para as operações LOAD, STOR, ADD, SUB, LSH e RSH, é o registrador AC que armazenará o operando ou o resultado.

- MQ (*Multiplier Quotient*)
	> Armazena temporariamente operandos e resultados de operações aritméticas.
	> Serve como registrador padrão, isto é, caso não seja explicitado um endereço para as operações MUL e DIV, é o registrador MQ que armazenará o operando ou o resultado.

- R (Resto da Divisão)
	> Armazena temporariamente o resto da operação de divisão.

- C (*Carry Out*)
	> Armazena temporariamente a informação se o resultado de uma operação pertence ao limite estipulado, o qual é de 10 bits. Dessa forma, o intervalo é de -1023 a 1024.
	> Se há carry, é setada como 1. Se não há, é setada como 0.

- Z (Resultado Zero)
	> Armazena temporariamente a informação se o resultado de uma operação é zero.
	> Se o resultado é igual a zero, é setada como 1. Se é diferente, é setada como 0.

### Presentes na Unidade de Controle (UC)

Registradores que armazenam partes da instrução.

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

- Registradores de uso geral
	> São eles: GERAL_A, GERAL_B, GERAL_C, GERAL_D.
	> Armazenam dados temporários durante a execução de instruções. 
	> São essenciais para operações aritméticas, lógicas e de controle.

- Variáveis auxiliares aos registradores
	> OFFSET_ARQ auxilia na manipulação do arquivo; 
	> USO_ULA auxilia na manipulação dos dados de operações lógicas e aritméticas;
	> BARRA_DADOS auxiliar na manipulação de dados durante as operações;

## Funções Auxiliares

### analisar_resultado
> Analisa se o resultado de uma operação está dentro do limite estipulado de 10 bits. Como o máximo definido é 10 bits, o intervalo é de -1023 a 1024.
### atualizar_registrador
> Atualiza o registrador correto com seu novo valor, isto é, o valor resultante da instrução executada.
### buscar_endereco
> Busca o endereço na memória e retorna o dado e sua posição na memória volátil se for endereçamento direto. Caso seja endereçamento imediato, retorna o próprio dado.
### buscar_instrucao
> Busca a próxima instrução no endereço apontado por PC.
### buscar_referencia
> Determina qual dado de registrador ou dado de memória a instrução precisa.
### carregar_memoria
> Carrega a memória volátil com os dados do arquivo.

## Funções Principais

### executar_LOAD
> Carrega um valor da memória no acumulador (AC) ou em outro registrador especificado: LOAD X | LOAD X, Y.
### executar_MOV
> Move dados de um registrador para outro: MOV X | MOV X, Y.
### executar_STOR
> Armazena um dado de um registrador na memória volátil. STOR X | STOR X, Y.
### executar_JUMP
> Executa um salto na execução sequencial das instruções: JUMP X : PC <- X.
### executar_JUMP_zero
> Executa um salto na execução sequencial das instruções se o AC for MAIOR ou igual a 0: JUMP+ X : PC <- X (A >= 0).
### executar_ADD
> Soma um dado ao acumulador ou a outro registrador especificado: ADD X | ADD X, Y.
### executar_SUB
> Subtrai um dado de AC ou outro registrador especificado: SUB X | SUB X, Y.
### executar_MUL
> Multiplica um dado X pelo MQ ou outro registrador especificado: MULT X | MULT X, Y.
### executar_DIV
> Divide o AC ou um registrador Y por um dado X: DIV X, Y; ou divide o AC pelo valor armazenado em X da memoria: DIV X.
### executar_LSH
> Desloca os bits do registrador AC para a esquerda. Equivale a multiplicar o valor em AC por 2.
### executar_RSH
> Desloca os bits do registrador AC para a direita. Equivale a dividir o valor em AC por 2.
### executar_instrucao
> Executa a instrução atual, e identifica qual instrução está sendo executada.

## Referências

BORIN, Edson; AULER, Rafael. Programando o computador IAS. UNICAMP, 2012. Disponível em: https://www.ic.unicamp.br/~edson/disciplinas/mc404/2012-1s/anexos/programando_o_IAS.pdf. Acesso em: 14 ago. 2024.

CALVO, Rodrigo. **Estruturas de Interconexão do Computador:** Arquitetura e Organização de Computadores I. Universidade Estadual de Maringá – UEM. Departamento de Informática – DIN. jul. 2024. Apresentação de Power Point. Acesso em: 14. ago. 2024.

CALVO, Rodrigo. **Conjunto de Instruções: Características e Funções:** Arquitetura e Organização de Computadores I. Universidade Estadual de Maringá – UEM. Departamento de Informática – DIN. jul. 2024. Apresentação de Power Point. Acesso em: 19. ago. 2024.

CALVO, Rodrigo. **Conjunto de Instruções: Modos de Endereçamento e Formatos:** Arquitetura e Organização de Computadores I. Universidade Estadual de Maringá – UEM. Departamento de Informática – DIN. jul. 2024. Apresentação de Power Point. Acesso em: 19. ago. 2024.
