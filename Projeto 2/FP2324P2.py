"""
Go
Segundo Projeto de Fundamentos da Programacao - 2023/2024

Autor: Joao Trigueiros Ferreira (ist1110573)
Curso: LEIC-A

O programa permite jogar ao Go num goban de 9x9, 13x13 ou 19x19 intersecoes.
Estao definidos tres tipos abstratos de dados (TAD), cada um construido apenas
sobre as operacoes basicas do TAD anterior.

TAD intersecao (imutavel)
    Representacao interna: tuplo (col, lin), em que col e uma letra maiuscula
    de 'A' a 'S' e lin um inteiro de 1 a 19. Por exemplo, ('B', 3).
    Operacoes basicas:
        cria_intersecao: str x int -> intersecao
        obtem_col: intersecao -> str
        obtem_lin: intersecao -> int
        eh_intersecao: universal -> booleano
        intersecoes_iguais: universal x universal -> booleano
        intersecao_para_str: intersecao -> str
        str_para_intersecao: str -> intersecao

TAD pedra (imutavel)
    Representacao interna: um dos inteiros PEDRA_BRANCA, PEDRA_PRETA ou
    PEDRA_NEUTRA, esta ultima usada para as intersecoes livres.
    Operacoes basicas:
        cria_pedra_branca: {} -> pedra
        cria_pedra_preta: {} -> pedra
        cria_pedra_neutra: {} -> pedra
        eh_pedra: universal -> booleano
        eh_pedra_branca: pedra -> booleano
        eh_pedra_preta: pedra -> booleano
        pedras_iguais: universal x universal -> booleano
        pedra_para_str: pedra -> str

TAD goban (mutavel)
    Representacao interna: lista de n listas de n pedras, uma lista por linha
    do goban, da linha 1 para a linha n e, dentro de cada linha, da coluna 'A'
    para a coluna n-esima. As intersecoes livres guardam uma pedra neutra.
    Operacoes basicas:
        cria_goban_vazio: int -> goban
        cria_goban: int x tuplo x tuplo -> goban
        cria_copia_goban: goban -> goban
        obtem_ultima_intersecao: goban -> intersecao
        obtem_pedra: goban x intersecao -> pedra
        obtem_cadeia: goban x intersecao -> tuplo
        coloca_pedra: goban x intersecao x pedra -> goban
        remove_pedra: goban x intersecao -> goban
        remove_cadeia: goban x tuplo -> goban
        eh_goban: universal -> booleano
        eh_intersecao_valida: goban x intersecao -> booleano
        gobans_iguais: universal x universal -> booleano
        goban_para_str: goban -> str

A ordem de leitura das intersecoes do goban e sempre da esquerda para a
direita, seguida de baixo para cima.
"""

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

PRIMEIRA_COLUNA = 'A'
ULTIMA_COLUNA = 'S'    # 'A' + 19 - 1
ULTIMA_LINHA = 19
DIMENSOES_VALIDAS = (9, 13, 19)

PEDRA_BRANCA = 1
PEDRA_PRETA = -1
PEDRA_NEUTRA = 0

# Representacao externa de cada pedra.
MARCAS = {PEDRA_BRANCA: 'O', PEDRA_PRETA: 'X', PEDRA_NEUTRA: '.'}

# As etiquetas das linhas sao alinhadas a direita em duas posicoes, para que
# os gobans de 19x19 fiquem com as colunas alinhadas.
LARGURA_ETIQUETA = 2

# Deslocamentos (coluna, linha) das intersecoes adjacentes, ja pela ordem de
# leitura do goban: baixo, esquerda, direita e cima.
DIRECOES_ADJACENTES = ((0, -1), (-1, 0), (1, 0), (0, 1))

PASSAR = 'P'
PEDIDO_JOGADA = "Escreva uma intersecao ou 'P' para passar [{}]:"


# ---------------------------------------------------------------------------
# TAD intersecao
# ---------------------------------------------------------------------------

def cria_intersecao(col, lin):
    """cria_intersecao: str x int -> intersecao

    Devolve a intersecao da coluna col e da linha lin, verificando a validade
    dos seus argumentos.
    """
    if not eh_intersecao((col, lin)):
        raise ValueError('cria_intersecao: argumentos invalidos')
    return (col, lin)


def obtem_col(i):
    """obtem_col: intersecao -> str

    Devolve a coluna da intersecao.
    """
    return i[0]


def obtem_lin(i):
    """obtem_lin: intersecao -> int

    Devolve a linha da intersecao.
    """
    return i[1]


def eh_intersecao(arg):
    """eh_intersecao: universal -> booleano

    Devolve True se o argumento corresponde a uma intersecao, isto e, a um
    tuplo com uma letra maiuscula de 'A' a 'S' e um inteiro de 1 a 19, e False
    caso contrario.
    """
    if not isinstance(arg, tuple) or len(arg) != 2:
        return False
    col, lin = arg
    return (isinstance(col, str) and len(col) == 1
            and PRIMEIRA_COLUNA <= col <= ULTIMA_COLUNA
            and isinstance(lin, int) and not isinstance(lin, bool)
            and 1 <= lin <= ULTIMA_LINHA)


def intersecoes_iguais(i1, i2):
    """intersecoes_iguais: universal x universal -> booleano

    Devolve True apenas se i1 e i2 sao intersecoes e sao iguais.
    """
    return (eh_intersecao(i1) and eh_intersecao(i2)
            and obtem_col(i1) == obtem_col(i2)
            and obtem_lin(i1) == obtem_lin(i2))


def intersecao_para_str(i):
    """intersecao_para_str: intersecao -> str

    Devolve a representacao externa da intersecao, por exemplo 'B13'.
    """
    return obtem_col(i) + str(obtem_lin(i))


def str_para_intersecao(s):
    """str_para_intersecao: str -> intersecao

    Devolve a intersecao representada pela cadeia de caracteres dada.
    """
    return cria_intersecao(s[0], int(s[1:]))


def obtem_intersecoes_adjacentes(i, l):
    """obtem_intersecoes_adjacentes: intersecao x intersecao -> tuplo

    Devolve o tuplo com as intersecoes adjacentes a intersecao i, pela ordem
    de leitura de um goban cuja intersecao superior direita e l.
    """
    adjacentes = ()
    for desloc_col, desloc_lin in DIRECOES_ADJACENTES:
        col = chr(ord(obtem_col(i)) + desloc_col)
        lin = obtem_lin(i) + desloc_lin
        # A intersecao adjacente so conta se nao sair fora do goban.
        if (PRIMEIRA_COLUNA <= col <= obtem_col(l)
                and 1 <= lin <= obtem_lin(l)):
            adjacentes += (cria_intersecao(col, lin),)
    return adjacentes


def ordena_intersecoes(t):
    """ordena_intersecoes: tuplo -> tuplo

    Devolve um tuplo com as mesmas intersecoes do tuplo dado (potencialmente
    vazio), ordenadas de acordo com a ordem de leitura do goban.
    """
    return tuple(sorted(t, key=lambda i: (obtem_lin(i), obtem_col(i))))


# ---------------------------------------------------------------------------
# TAD pedra
# ---------------------------------------------------------------------------

def cria_pedra_branca():
    """cria_pedra_branca: {} -> pedra

    Devolve uma pedra do jogador branco.
    """
    return PEDRA_BRANCA


def cria_pedra_preta():
    """cria_pedra_preta: {} -> pedra

    Devolve uma pedra do jogador preto.
    """
    return PEDRA_PRETA


def cria_pedra_neutra():
    """cria_pedra_neutra: {} -> pedra

    Devolve uma pedra neutra, isto e, que nao pertence a nenhum jogador.
    """
    return PEDRA_NEUTRA


def eh_pedra(arg):
    """eh_pedra: universal -> booleano

    Devolve True se o argumento corresponde a uma pedra e False caso
    contrario.
    """
    return (isinstance(arg, int) and not isinstance(arg, bool)
            and arg in MARCAS)


def eh_pedra_branca(p):
    """eh_pedra_branca: pedra -> booleano

    Devolve True se a pedra pertence ao jogador branco e False caso contrario.
    """
    return p == PEDRA_BRANCA


def eh_pedra_preta(p):
    """eh_pedra_preta: pedra -> booleano

    Devolve True se a pedra pertence ao jogador preto e False caso contrario.
    """
    return p == PEDRA_PRETA


def pedras_iguais(p1, p2):
    """pedras_iguais: universal x universal -> booleano

    Devolve True apenas se p1 e p2 sao pedras e sao iguais.
    """
    return eh_pedra(p1) and eh_pedra(p2) and p1 == p2


def pedra_para_str(p):
    """pedra_para_str: pedra -> str

    Devolve a representacao externa da pedra: 'O' para o jogador branco, 'X'
    para o jogador preto e '.' para a pedra neutra.
    """
    return MARCAS[p]


def eh_pedra_jogador(p):
    """eh_pedra_jogador: pedra -> booleano

    Devolve True se a pedra pertence a um dos jogadores e False caso
    contrario.
    """
    return eh_pedra_branca(p) or eh_pedra_preta(p)


def obtem_pedra_adversaria(p):
    """obtem_pedra_adversaria: pedra -> pedra

    Devolve a pedra do jogador adversario do dono da pedra dada.
    """
    return cria_pedra_preta() if eh_pedra_branca(p) else cria_pedra_branca()


# ---------------------------------------------------------------------------
# TAD goban
# ---------------------------------------------------------------------------

def eh_dimensao_valida(n):
    """eh_dimensao_valida: universal -> booleano

    Devolve True se o argumento corresponde a uma dimensao possivel de um
    goban e False caso contrario.
    """
    return (isinstance(n, int) and not isinstance(n, bool)
            and n in DIMENSOES_VALIDAS)


def cria_goban_vazio(n):
    """cria_goban_vazio: int -> goban

    Devolve um goban de tamanho n x n sem intersecoes ocupadas, verificando a
    validade do seu argumento.
    """
    if not eh_dimensao_valida(n):
        raise ValueError('cria_goban_vazio: argumento invalido')
    return [[cria_pedra_neutra() for _ in range(n)] for _ in range(n)]


def cria_goban(n, ib, ip):
    """cria_goban: int x tuplo x tuplo -> goban

    Devolve um goban de tamanho n x n com as intersecoes do tuplo ib ocupadas
    por pedras brancas e as do tuplo ip ocupadas por pedras pretas,
    verificando a validade dos seus argumentos.
    """
    if (not eh_dimensao_valida(n)
            or not isinstance(ib, tuple) or not isinstance(ip, tuple)):
        raise ValueError('cria_goban: argumentos invalidos')

    goban = cria_goban_vazio(n)
    for intersecoes, pedra in ((ib, cria_pedra_branca()), (ip, cria_pedra_preta())):
        for i in intersecoes:
            # Uma intersecao ja ocupada denuncia repeticoes dentro de um dos
            # tuplos ou entre os dois tuplos.
            if (not eh_intersecao(i) or not eh_intersecao_valida(goban, i)
                    or eh_pedra_jogador(obtem_pedra(goban, i))):
                raise ValueError('cria_goban: argumentos invalidos')
            coloca_pedra(goban, i, pedra)
    return goban


def cria_copia_goban(t):
    """cria_copia_goban: goban -> goban

    Devolve uma copia nova do goban dado.
    """
    return [linha[:] for linha in t]


def obtem_ultima_intersecao(g):
    """obtem_ultima_intersecao: goban -> intersecao

    Devolve a intersecao do canto superior direito do goban.
    """
    return cria_intersecao(chr(ord(PRIMEIRA_COLUNA) + len(g) - 1), len(g))


def obtem_pedra(g, i):
    """obtem_pedra: goban x intersecao -> pedra

    Devolve a pedra que ocupa a intersecao i do goban g, ou uma pedra neutra
    se a intersecao estiver livre.
    """
    return g[obtem_lin(i) - 1][ord(obtem_col(i)) - ord(PRIMEIRA_COLUNA)]


def obtem_cadeia(g, i):
    """obtem_cadeia: goban x intersecao -> tuplo

    Devolve o tuplo com as intersecoes, em ordem de leitura, da cadeia que
    passa pela intersecao i. Se a intersecao estiver livre, devolve a cadeia
    de intersecoes livres a que pertence.
    """
    # Travessia em largura a partir de i, avancando apenas para intersecoes
    # adjacentes ocupadas pelo mesmo tipo de pedra.
    ultima = obtem_ultima_intersecao(g)
    pedra = obtem_pedra(g, i)
    cadeia = {i}
    por_visitar = [i]

    while por_visitar:
        atual = por_visitar.pop()
        for adjacente in obtem_intersecoes_adjacentes(atual, ultima):
            if (adjacente not in cadeia
                    and pedras_iguais(obtem_pedra(g, adjacente), pedra)):
                cadeia.add(adjacente)
                por_visitar.append(adjacente)

    return ordena_intersecoes(tuple(cadeia))


def coloca_pedra(g, i, p):
    """coloca_pedra: goban x intersecao x pedra -> goban

    Modifica destrutivamente o goban g, colocando a pedra p na intersecao i, e
    devolve o proprio goban.
    """
    g[obtem_lin(i) - 1][ord(obtem_col(i)) - ord(PRIMEIRA_COLUNA)] = p
    return g


def remove_pedra(g, i):
    """remove_pedra: goban x intersecao -> goban

    Modifica destrutivamente o goban g, removendo a pedra da intersecao i, e
    devolve o proprio goban.
    """
    return coloca_pedra(g, i, cria_pedra_neutra())


def remove_cadeia(g, t):
    """remove_cadeia: goban x tuplo -> goban

    Modifica destrutivamente o goban g, removendo as pedras das intersecoes do
    tuplo t, e devolve o proprio goban.
    """
    for i in t:
        remove_pedra(g, i)
    return g


def eh_goban(arg):
    """eh_goban: universal -> booleano

    Devolve True se o argumento corresponde a um goban, isto e, a uma lista de
    n listas de n pedras com n uma dimensao valida, e False caso contrario.
    """
    if not isinstance(arg, list) or not eh_dimensao_valida(len(arg)):
        return False
    return all(isinstance(linha, list) and len(linha) == len(arg)
               and all(eh_pedra(pedra) for pedra in linha)
               for linha in arg)


def eh_intersecao_valida(g, i):
    """eh_intersecao_valida: goban x intersecao -> booleano

    Devolve True se i e uma intersecao dentro do goban g e False caso
    contrario.
    """
    ultima = obtem_ultima_intersecao(g)
    return (eh_intersecao(i) and obtem_col(i) <= obtem_col(ultima)
            and obtem_lin(i) <= obtem_lin(ultima))


def gobans_iguais(g1, g2):
    """gobans_iguais: universal x universal -> booleano

    Devolve True apenas se g1 e g2 sao gobans e sao iguais.
    """
    return eh_goban(g1) and eh_goban(g2) and g1 == g2


def goban_para_str(g):
    """goban_para_str: goban -> str

    Devolve a representacao externa do goban: as pedras de cada intersecao
    ladeadas pelos identificadores das linhas e das colunas.
    """
    ultima = obtem_ultima_intersecao(g)
    colunas = obtem_colunas(g)
    # As colunas sao alinhadas com as pedras que lhes ficam por baixo.
    cabecalho = ' ' * (LARGURA_ETIQUETA + 1) + ' '.join(colunas)

    linhas = [cabecalho]
    for lin in range(obtem_lin(ultima), 0, -1):  # de cima para baixo
        pedras = ' '.join(pedra_para_str(obtem_pedra(g, cria_intersecao(col, lin)))
                          for col in colunas)
        linhas.append('{} {} {}'.format(str(lin).rjust(LARGURA_ETIQUETA),
                                        pedras, lin))
    linhas.append(cabecalho)

    return '\n'.join(linhas)


def obtem_colunas(g):
    """obtem_colunas: goban -> tuplo

    Devolve o tuplo com os identificadores das colunas do goban, da esquerda
    para a direita.
    """
    ultima_col = obtem_col(obtem_ultima_intersecao(g))
    return tuple(chr(col)
                 for col in range(ord(PRIMEIRA_COLUNA), ord(ultima_col) + 1))


def obtem_intersecoes(g):
    """obtem_intersecoes: goban -> tuplo

    Devolve o tuplo com todas as intersecoes do goban, pela ordem de leitura
    do goban.
    """
    ultima = obtem_ultima_intersecao(g)
    return tuple(cria_intersecao(col, lin)
                 for lin in range(1, obtem_lin(ultima) + 1)
                 for col in obtem_colunas(g))


def obtem_territorios(g):
    """obtem_territorios: goban -> tuplo

    Devolve o tuplo formado pelos tuplos com as intersecoes de cada territorio
    do goban. As intersecoes de cada territorio sao devolvidas em ordem de
    leitura, e os territorios ordenados pela sua primeira intersecao.
    """
    visitadas = set()
    territorios = ()
    for i in obtem_intersecoes(g):
        # Cada intersecao livre ainda nao visitada da inicio a um territorio.
        if i not in visitadas and not eh_pedra_jogador(obtem_pedra(g, i)):
            territorio = obtem_cadeia(g, i)
            visitadas.update(territorio)
            territorios += (territorio,)
    return territorios


def obtem_adjacentes_diferentes(g, t):
    """obtem_adjacentes_diferentes: goban x tuplo -> tuplo

    Devolve o tuplo ordenado com as intersecoes adjacentes as intersecoes do
    tuplo t que estao no estado oposto: as liberdades, se t for uma cadeia de
    pedras de um jogador, ou a fronteira, se t for um territorio.
    """
    ultima = obtem_ultima_intersecao(g)
    diferentes = set()
    for i in t:
        livre = not eh_pedra_jogador(obtem_pedra(g, i))
        for adjacente in obtem_intersecoes_adjacentes(i, ultima):
            if eh_pedra_jogador(obtem_pedra(g, adjacente)) == livre:
                diferentes.add(adjacente)
    return ordena_intersecoes(tuple(diferentes))


def jogada(g, i, p):
    """jogada: goban x intersecao x pedra -> goban

    Modifica destrutivamente o goban g, colocando a pedra p na intersecao i e
    capturando as cadeias adversarias adjacentes que ficam sem liberdades, e
    devolve o proprio goban.
    """
    coloca_pedra(g, i, p)

    adversaria = obtem_pedra_adversaria(p)
    for adjacente in obtem_intersecoes_adjacentes(i, obtem_ultima_intersecao(g)):
        if pedras_iguais(obtem_pedra(g, adjacente), adversaria):
            cadeia = obtem_cadeia(g, adjacente)
            if obtem_adjacentes_diferentes(g, cadeia) == ():
                remove_cadeia(g, cadeia)
    return g


def obtem_pedras_jogadores(g):
    """obtem_pedras_jogadores: goban -> tuplo

    Devolve o tuplo com o numero de intersecoes ocupadas por pedras do jogador
    branco e do jogador preto, respetivamente.
    """
    pedras = tuple(obtem_pedra(g, i) for i in obtem_intersecoes(g))
    return (sum(1 for p in pedras if eh_pedra_branca(p)),
            sum(1 for p in pedras if eh_pedra_preta(p)))


# ---------------------------------------------------------------------------
# Funcoes adicionais
# ---------------------------------------------------------------------------

def calcula_pontos(g):
    """calcula_pontos: goban -> tuplo

    Devolve o tuplo com as pontuacoes dos jogadores branco e preto, isto e, o
    numero de intersecoes ocupadas pelas suas pedras somado ao numero de
    intersecoes dos territorios que lhes pertencem.
    """
    brancas, pretas = obtem_pedras_jogadores(g)

    for territorio in obtem_territorios(g):
        fronteira = obtem_adjacentes_diferentes(g, territorio)
        # Um territorio sem fronteira (o goban vazio) nao pertence a ninguem.
        if fronteira == ():
            continue
        pedras = tuple(obtem_pedra(g, i) for i in fronteira)
        if all(eh_pedra_branca(p) for p in pedras):
            brancas += len(territorio)
        elif all(eh_pedra_preta(p) for p in pedras):
            pretas += len(territorio)

    return (brancas, pretas)


def eh_jogada_legal(g, i, p, l):
    """eh_jogada_legal: goban x intersecao x pedra x goban -> booleano

    Devolve True se colocar a pedra p na intersecao i do goban g e uma jogada
    legal e False caso contrario, sem modificar g nem l. O goban l representa
    o estado que nao pode ser obtido depois da jogada (regra do ko).
    """
    if not eh_intersecao_valida(g, i) or eh_pedra_jogador(obtem_pedra(g, i)):
        return False

    hipotese = jogada(cria_copia_goban(g), i, p)

    # Regra do suicidio: a cadeia jogada tem de ficar com liberdades.
    if obtem_adjacentes_diferentes(hipotese, obtem_cadeia(hipotese, i)) == ():
        return False

    # Regra da repeticao: o estado obtido nao pode ser um estado anterior.
    return not gobans_iguais(hipotese, l)


def eh_str_intersecao(arg):
    """eh_str_intersecao: universal -> booleano

    Devolve True se o argumento corresponde a representacao externa de uma
    intersecao e False caso contrario.
    """
    return (isinstance(arg, str) and len(arg) > 1
            and arg[1:].isdigit() and arg[1] != '0'
            and eh_intersecao((arg[0], int(arg[1:]))))


def turno_jogador(g, p, l):
    """turno_jogador: goban x pedra x goban -> booleano

    Oferece ao jogador das pedras p a opcao de passar ou de jogar numa
    intersecao, repetindo o pedido ate a resposta ser 'P' ou uma jogada legal.
    Se o jogador passar devolve False sem modificar os argumentos; caso
    contrario modifica destrutivamente o goban g e devolve True.
    """
    while True:
        escolha = input(PEDIDO_JOGADA.format(pedra_para_str(p)))
        if escolha == PASSAR:
            return False
        if eh_str_intersecao(escolha):
            i = str_para_intersecao(escolha)
            if eh_jogada_legal(g, i, p, l):
                jogada(g, i, p)
                return True


def mostra_estado(g):
    """mostra_estado: goban -> {}

    Escreve no ecra a pontuacao de cada jogador e o estado atual do goban.
    """
    brancas, pretas = calcula_pontos(g)
    print('Branco (O) tem {} pontos'.format(brancas))
    print('Preto (X) tem {} pontos'.format(pretas))
    print(goban_para_str(g))


def go(n, tb, tp):
    """go: int x tuplo x tuplo -> booleano

    Permite jogar um jogo completo de Go num goban de tamanho n x n, com as
    intersecoes dos tuplos tb e tp inicialmente ocupadas por pedras brancas e
    pretas, respetivamente. O jogo termina quando os dois jogadores passam a
    vez consecutivamente. Devolve True se o jogador branco ganhar o jogo (o
    que inclui o empate) e False caso contrario.
    """
    if (not eh_dimensao_valida(n)
            or not isinstance(tb, tuple) or not isinstance(tp, tuple)
            or not all(eh_str_intersecao(s) for s in tb + tp)):
        raise ValueError('go: argumentos invalidos')
    try:
        g = cria_goban(n, tuple(str_para_intersecao(s) for s in tb),
                       tuple(str_para_intersecao(s) for s in tp))
    except ValueError:
        raise ValueError('go: argumentos invalidos')

    jogadores = (cria_pedra_preta(), cria_pedra_branca())  # o preto comeca
    proibido = cria_goban_vazio(n)  # estado proibido pela regra do ko
    passou = False
    turno = 0

    while True:
        mostra_estado(g)
        estado_atual = cria_copia_goban(g)
        jogou = turno_jogador(g, jogadores[turno % 2], proibido)
        if not jogou and passou:
            break
        # A jogada seguinte nao pode repor o estado anterior a jogada atual.
        proibido, passou = estado_atual, not jogou
        turno += 1

    mostra_estado(g)
    brancas, pretas = calcula_pontos(g)
    return brancas >= pretas
