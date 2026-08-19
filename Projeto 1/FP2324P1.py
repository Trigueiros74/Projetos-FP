"""
Montanhas e Vales
Primeiro Projeto de Fundamentos da Programacao - 2023/2024

Autor: Joao Trigueiros Ferreira (ist1110573)
Curso: LEIC-A

Um territorio e representado por um tuplo de Nv tuplos (os caminhos verticais,
identificados por letras de 'A' a 'Z'), cada um com Nh inteiros (os caminhos
horizontais, identificados por numeros de 1 a 99). O valor 0 corresponde a uma
intersecao livre e o valor 1 a uma intersecao ocupada por uma montanha.

Uma intersecao e representada por um tuplo de dois elementos (letra, numero),
por exemplo ('B', 3).

A ordem de leitura de um territorio e sempre da esquerda para a direita,
seguida de baixo para cima.
"""

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

LIVRE = 0
MONTANHA = 1

MARCA_LIVRE = '.'
MARCA_MONTANHA = 'X'

MAX_CAMINHOS_VERTICAIS = 26    # 'A' a 'Z'
MAX_CAMINHOS_HORIZONTAIS = 99  # 1 a 99

# Deslocamentos (coluna, linha) das intersecoes adjacentes, ja pela ordem de
# leitura de um territorio: baixo, esquerda, direita e cima.
DIRECOES_ADJACENTES = ((0, -1), (-1, 0), (1, 0), (0, 1))


# ---------------------------------------------------------------------------
# Funcoes auxiliares
# ---------------------------------------------------------------------------

def intersecao_para_indices(intersecao):
    """intersecao_para_indices: intersecao -> tuplo

    Devolve o par de indices (coluna, linha) que localiza a intersecao dentro
    da representacao interna de um territorio.
    """
    letra, numero = intersecao
    return ord(letra) - ord('A'), numero - 1


def indices_para_intersecao(coluna, linha):
    """indices_para_intersecao: int x int -> intersecao

    Operacao inversa de intersecao_para_indices.
    """
    return chr(ord('A') + coluna), linha + 1


def obtem_valor_intersecao(territorio, intersecao):
    """obtem_valor_intersecao: territorio x intersecao -> int

    Devolve o conteudo (LIVRE ou MONTANHA) de uma intersecao do territorio.
    """
    coluna, linha = intersecao_para_indices(intersecao)
    return territorio[coluna][linha]


def obtem_intersecoes(territorio):
    """obtem_intersecoes: territorio -> tuplo

    Devolve o tuplo com todas as intersecoes do territorio, pela ordem de
    leitura do territorio.
    """
    ultima_letra, ultimo_numero = obtem_ultima_intersecao(territorio)
    return tuple((chr(letra), numero)
                 for numero in range(1, ultimo_numero + 1)
                 for letra in range(ord('A'), ord(ultima_letra) + 1))


# ---------------------------------------------------------------------------
# Funcoes de manipulacao do territorio e das intersecoes
# ---------------------------------------------------------------------------

def eh_territorio(arg):
    """eh_territorio: universal -> booleano

    Devolve True se o argumento corresponde a um territorio, isto e, a um
    tuplo nao vazio de tuplos nao vazios do mesmo comprimento, contendo apenas
    os valores LIVRE e MONTANHA, e False caso contrario.
    """
    if not isinstance(arg, tuple) or not 1 <= len(arg) <= MAX_CAMINHOS_VERTICAIS:
        return False
    if not all(isinstance(caminho, tuple) for caminho in arg):
        return False
    if not 1 <= len(arg[0]) <= MAX_CAMINHOS_HORIZONTAIS:
        return False
    return all(len(caminho) == len(arg[0]) and
               all(isinstance(valor, int) and valor in (LIVRE, MONTANHA)
                   for valor in caminho)
               for caminho in arg)


def obtem_ultima_intersecao(territorio):
    """obtem_ultima_intersecao: territorio -> intersecao

    Devolve a intersecao do extremo superior direito do territorio.
    """
    return indices_para_intersecao(len(territorio) - 1, len(territorio[0]) - 1)


def eh_intersecao(arg):
    """eh_intersecao: universal -> booleano

    Devolve True se o argumento corresponde a uma intersecao, isto e, a um
    tuplo com uma letra maiuscula de 'A' a 'Z' e um inteiro de 1 a 99, e False
    caso contrario.
    """
    if not isinstance(arg, tuple) or len(arg) != 2:
        return False
    letra, numero = arg
    return (isinstance(letra, str) and len(letra) == 1 and 'A' <= letra <= 'Z'
            and isinstance(numero, int)
            and 1 <= numero <= MAX_CAMINHOS_HORIZONTAIS)


def eh_intersecao_valida(territorio, intersecao):
    """eh_intersecao_valida: territorio x intersecao -> booleano

    Devolve True se a intersecao pertence ao territorio e False caso
    contrario.
    """
    if not eh_territorio(territorio) or not eh_intersecao(intersecao):
        return False
    ultima_letra, ultimo_numero = obtem_ultima_intersecao(territorio)
    return intersecao[0] <= ultima_letra and intersecao[1] <= ultimo_numero


def eh_intersecao_livre(territorio, intersecao):
    """eh_intersecao_livre: territorio x intersecao -> booleano

    Devolve True se a intersecao pertence ao territorio e nao esta ocupada por
    uma montanha, e False caso contrario.
    """
    return (eh_intersecao_valida(territorio, intersecao) and
            obtem_valor_intersecao(territorio, intersecao) == LIVRE)


def obtem_intersecoes_adjacentes(territorio, intersecao):
    """obtem_intersecoes_adjacentes: territorio x intersecao -> tuplo

    Devolve o tuplo das intersecoes validas adjacentes a intersecao dada, pela
    ordem de leitura do territorio.
    """
    ultima_letra, ultimo_numero = obtem_ultima_intersecao(territorio)
    coluna, linha = intersecao_para_indices(intersecao)

    adjacentes = ()
    for desloc_coluna, desloc_linha in DIRECOES_ADJACENTES:
        letra, numero = indices_para_intersecao(coluna + desloc_coluna,
                                                linha + desloc_linha)
        # A intersecao adjacente so conta se nao sair fora do territorio.
        if 'A' <= letra <= ultima_letra and 1 <= numero <= ultimo_numero:
            adjacentes += ((letra, numero),)
    return adjacentes


def ordena_intersecoes(tup):
    """ordena_intersecoes: tuplo -> tuplo

    Devolve um tuplo com as mesmas intersecoes do tuplo dado (potencialmente
    vazio), ordenadas de acordo com a ordem de leitura do territorio.
    """
    return tuple(sorted(tup, key=lambda intersecao: (intersecao[1], intersecao[0])))


def territorio_para_str(territorio):
    """territorio_para_str: territorio -> cad. carateres

    Devolve a representacao externa do territorio: as montanhas sao marcadas
    com 'X' e as intersecoes livres com '.', ladeadas pelos identificadores
    dos caminhos horizontais e verticais.
    """
    if not eh_territorio(territorio):
        raise ValueError('territorio_para_str: argumento invalido')

    ultima_letra, ultimo_numero = obtem_ultima_intersecao(territorio)
    letras = (chr(letra) for letra in range(ord('A'), ord(ultima_letra) + 1))
    caminhos_verticais = '   ' + ' '.join(letras)

    linhas = [caminhos_verticais]
    for numero in range(ultimo_numero, 0, -1):  # de cima para baixo
        # As etiquetas dos caminhos horizontais ocupam sempre duas posicoes.
        etiqueta = str(numero).rjust(2)
        marcas = ' '.join(MARCA_LIVRE if valor == LIVRE else MARCA_MONTANHA
                          for valor in (caminho[numero - 1] for caminho in territorio))
        linhas.append('{} {} {}'.format(etiqueta, marcas, etiqueta))
    linhas.append(caminhos_verticais)

    return '\n'.join(linhas)


# ---------------------------------------------------------------------------
# Funcoes das cadeias de montanhas e dos vales
# ---------------------------------------------------------------------------

def obtem_cadeia(territorio, intersecao):
    """obtem_cadeia: territorio x intersecao -> tuplo

    Devolve o tuplo com todas as intersecoes conetadas a intersecao dada
    (incluindo-a), ordenadas de acordo com a ordem de leitura do territorio.
    Uma cadeia e formada apenas por intersecoes todas livres ou todas ocupadas.
    """
    if not eh_intersecao_valida(territorio, intersecao):
        raise ValueError('obtem_cadeia: argumentos invalidos')

    # Travessia em largura a partir da intersecao dada, avancando apenas para
    # intersecoes adjacentes com o mesmo estado (livre ou ocupada).
    estado = obtem_valor_intersecao(territorio, intersecao)
    cadeia = {intersecao}
    por_visitar = [intersecao]

    while por_visitar:
        atual = por_visitar.pop()
        for adjacente in obtem_intersecoes_adjacentes(territorio, atual):
            if (adjacente not in cadeia and
                    obtem_valor_intersecao(territorio, adjacente) == estado):
                cadeia.add(adjacente)
                por_visitar.append(adjacente)

    return ordena_intersecoes(tuple(cadeia))


def obtem_vale(territorio, intersecao):
    """obtem_vale: territorio x intersecao -> tuplo

    Devolve o tuplo (potencialmente vazio) com todas as intersecoes livres
    adjacentes a cadeia de montanhas da intersecao dada, ordenadas de acordo
    com a ordem de leitura do territorio.
    """
    if (not eh_intersecao_valida(territorio, intersecao) or
            eh_intersecao_livre(territorio, intersecao)):
        raise ValueError('obtem_vale: argumentos invalidos')

    vale = set()
    for montanha in obtem_cadeia(territorio, intersecao):
        for adjacente in obtem_intersecoes_adjacentes(territorio, montanha):
            if eh_intersecao_livre(territorio, adjacente):
                vale.add(adjacente)

    return ordena_intersecoes(tuple(vale))


# ---------------------------------------------------------------------------
# Funcoes de informacao de um territorio
# ---------------------------------------------------------------------------

def verifica_conexao(territorio, intersecao1, intersecao2):
    """verifica_conexao: territorio x intersecao x intersecao -> booleano

    Devolve True se as duas intersecoes do territorio estao conetadas, isto e,
    se pertencem a mesma cadeia, e False caso contrario.
    """
    if (not eh_intersecao_valida(territorio, intersecao1) or
            not eh_intersecao_valida(territorio, intersecao2)):
        raise ValueError('verifica_conexao: argumentos invalidos')

    return intersecao2 in obtem_cadeia(territorio, intersecao1)


def calcula_numero_montanhas(territorio):
    """calcula_numero_montanhas: territorio -> int

    Devolve o numero de intersecoes ocupadas por montanhas no territorio.
    """
    if not eh_territorio(territorio):
        raise ValueError('calcula_numero_montanhas: argumento invalido')

    return sum(caminho.count(MONTANHA) for caminho in territorio)


def calcula_numero_cadeias_montanhas(territorio):
    """calcula_numero_cadeias_montanhas: territorio -> int

    Devolve o numero de cadeias de montanhas contidas no territorio.
    """
    if not eh_territorio(territorio):
        raise ValueError('calcula_numero_cadeias_montanhas: argumento invalido')

    visitadas = set()
    cadeias = 0
    for intersecao in obtem_intersecoes(territorio):
        # Cada montanha ainda nao visitada da inicio a uma nova cadeia.
        if intersecao not in visitadas and not eh_intersecao_livre(territorio, intersecao):
            visitadas.update(obtem_cadeia(territorio, intersecao))
            cadeias += 1

    return cadeias


def calcula_tamanho_vales(territorio):
    """calcula_tamanho_vales: territorio -> int

    Devolve o numero total de intersecoes diferentes que formam todos os vales
    do territorio.
    """
    if not eh_territorio(territorio):
        raise ValueError('calcula_tamanho_vales: argumento invalido')

    montanhas_visitadas = set()
    vales = set()
    for intersecao in obtem_intersecoes(territorio):
        # Basta calcular o vale uma vez por cadeia de montanhas.
        if (intersecao not in montanhas_visitadas and
                not eh_intersecao_livre(territorio, intersecao)):
            montanhas_visitadas.update(obtem_cadeia(territorio, intersecao))
            vales.update(obtem_vale(territorio, intersecao))

    return len(vales)
