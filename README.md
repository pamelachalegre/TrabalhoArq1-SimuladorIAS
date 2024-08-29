# Simulador do Computador IAS

aqui será explicado o que é o ias

## Descrição

aqui será explicado o que foi pedido no trabalho e o que fizemos(?)

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

executar_LOAD

### Auxiliares

## Referências

BORIN, Edson; AULER, Rafael. Programando o computador IAS. UNICAMP, 2012. Disponível em: https://www.ic.unicamp.br/~edson/disciplinas/mc404/2012-1s/anexos/programando_o_IAS.pdf. Acesso em: 14 ago. 2024.

colocar os materiais do calvo aqui tb
