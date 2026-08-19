# Go

Segundo projeto de **Fundamentos da Programação** (LEIC-A, Instituto Superior Técnico, 2023/2024).

O programa permite jogar ao [Go](https://en.wikipedia.org/wiki/Go_(game)) para dois jogadores num **goban** de 9×9, 13×13 ou 19×19 interseções. Os jogadores colocam alternadamente pedras da sua cor, capturam as **cadeias** adversárias que ficam sem **liberdades** e ganha quem controlar o maior **território**.

```text
   A B C D E F G H I
 9 . . . . . . . . . 9
 8 . . . . . . . . . 8
 7 . . . . . . X . . 7
 6 . . . . . . X . . 6
 5 . . . . X X . . . 5
 4 . . . O X X . . . 4
 3 O O O O . . . . . 3
 2 . . O O . . . . . 2
 1 . . O . . . . . . 1
   A B C D E F G H I
```

Neste goban o branco (`O`) tem 12 pontos — 8 pedras mais o território de 4 interseções no canto inferior esquerdo — e o preto (`X`) tem 6.

## Regras implementadas

- **Captura** — depois de colocada a pedra, saem do tabuleiro as cadeias adversárias adjacentes que ficaram sem liberdades.
- **Suicídio** — é ilegal a jogada que deixe a cadeia do próprio jogador sem liberdades.
- **Repetição (ko)** — é ilegal a jogada que reponha um estado anterior do tabuleiro.
- **Pontuação** — cada jogador soma as interseções ocupadas pelas suas pedras às dos territórios cuja fronteira é apenas da sua cor. Em caso de empate ganha o branco.

## Tipos abstratos de dados

A solução está organizada em três TAD, cada um construído apenas sobre as operações básicas do anterior.

| TAD | Mutável | Representação interna |
| --- | --- | --- |
| `intersecao` | não | Tuplo `(col, lin)`, com uma letra de `'A'` a `'S'` e um inteiro de 1 a 19 — por exemplo `('B', 3)`. |
| `pedra` | não | Inteiro: `1` (branca), `-1` (preta) e `0` (neutra, usada nas interseções livres). |
| `goban` | sim | Lista de *n* listas de *n* pedras, uma lista por linha, da linha 1 para a linha *n*. |

## Como executar

Só precisas de Python 3 — o projeto não tem dependências.

```bash
python3 -i "FP2324P2.py"
```

```python
>>> go(9, (), ())          # jogo completo, tabuleiro vazio
>>> go(9, ('C1', 'C2'), ('E4', 'F4'))   # com pedras iniciais
```

Ou usando as funções diretamente:

```python
>>> ib = tuple(str_para_intersecao(i) for i in ('C1','C2','C3','D2','D3','D4','A3','B3'))
>>> ip = tuple(str_para_intersecao(i) for i in ('E4','E5','F4','F5','G6','G7'))
>>> g = cria_goban(9, ib, ip)
>>> cadeia = obtem_cadeia(g, cria_intersecao('F', 5))
>>> tuple(intersecao_para_str(i) for i in cadeia)
('E4', 'F4', 'E5', 'F5')
>>> tuple(intersecao_para_str(i) for i in obtem_adjacentes_diferentes(g, cadeia))
('E3', 'F3', 'G4', 'D5', 'G5', 'E6', 'F6')
>>> obtem_pedras_jogadores(g)
(8, 6)
>>> calcula_pontos(g)
(12, 6)
```

## Funções

### TAD `intersecao`

| Função | Descrição |
| --- | --- |
| `cria_intersecao(col, lin)` | Interseção da coluna `col` e da linha `lin`. |
| `obtem_col(i)` / `obtem_lin(i)` | Coluna e linha da interseção. |
| `eh_intersecao(arg)` | Verifica se o argumento é uma interseção. |
| `intersecoes_iguais(i1, i2)` | Verifica se são duas interseções iguais. |
| `intersecao_para_str(i)` / `str_para_intersecao(s)` | Conversão de e para a representação externa (`'B13'`). |
| `obtem_intersecoes_adjacentes(i, l)` | Interseções adjacentes, por ordem de leitura. |
| `ordena_intersecoes(t)` | Ordena interseções pela ordem de leitura. |

### TAD `pedra`

| Função | Descrição |
| --- | --- |
| `cria_pedra_branca()` / `cria_pedra_preta()` / `cria_pedra_neutra()` | Construtores das pedras. |
| `eh_pedra(arg)` | Verifica se o argumento é uma pedra. |
| `eh_pedra_branca(p)` / `eh_pedra_preta(p)` | Verifica a quem pertence a pedra. |
| `pedras_iguais(p1, p2)` | Verifica se são duas pedras iguais. |
| `pedra_para_str(p)` | Representação externa: `'O'`, `'X'` ou `'.'`. |
| `eh_pedra_jogador(p)` | Verifica se a pedra pertence a um jogador. |

### TAD `goban`

| Função | Descrição |
| --- | --- |
| `cria_goban_vazio(n)` | Goban *n*×*n* sem interseções ocupadas. |
| `cria_goban(n, ib, ip)` | Goban *n*×*n* com as pedras brancas e pretas indicadas. |
| `cria_copia_goban(g)` | Cópia independente do goban. |
| `obtem_ultima_intersecao(g)` | Interseção do canto superior direito. |
| `obtem_pedra(g, i)` | Pedra que ocupa a interseção. |
| `obtem_cadeia(g, i)` | Cadeia (de pedras ou de interseções livres) que passa pela interseção. |
| `coloca_pedra(g, i, p)` / `remove_pedra(g, i)` / `remove_cadeia(g, t)` | Modificam destrutivamente o goban. |
| `eh_goban(arg)` | Verifica se o argumento é um goban. |
| `eh_intersecao_valida(g, i)` | Verifica se a interseção pertence ao goban. |
| `gobans_iguais(g1, g2)` | Verifica se são dois gobans iguais. |
| `goban_para_str(g)` | Representação externa do goban. |
| `obtem_territorios(g)` | Interseções de cada território, por ordem de leitura. |
| `obtem_adjacentes_diferentes(g, t)` | Liberdades de uma cadeia ou fronteira de um território. |
| `jogada(g, i, p)` | Coloca a pedra e captura as cadeias adversárias sem liberdades. |
| `obtem_pedras_jogadores(g)` | Número de pedras de cada jogador. |

### Funções adicionais

| Função | Descrição |
| --- | --- |
| `calcula_pontos(g)` | Pontuação dos jogadores branco e preto. |
| `eh_jogada_legal(g, i, p, l)` | Verifica a jogada face às regras do suicídio e do ko. |
| `turno_jogador(g, p, l)` | Pede ao jogador que passe ou jogue, até a jogada ser legal. |
| `go(n, tb, tp)` | Jogo completo; devolve `True` se o jogador branco ganhar. |

A ordem de leitura das interseções do goban é sempre da esquerda para a direita, seguida de baixo para cima.

## Ficheiros

- `FP2324P2.py` — solução completa (ficheiro único, apenas built-ins do Python 3)
- `FP2324P2.md` — enunciado do projeto

---

Autor: João Trigueiros Ferreira (`ist1110573`).
