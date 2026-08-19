# Montanhas e Vales

Primeiro projeto de **Fundamentos da Programação** (LEIC-A, Instituto Superior Técnico, 2023/2024).

O programa analisa um **território** retangular formado por caminhos verticais (`A`–`Z`) e horizontais (`1`–`99`), cujas interseções podem estar livres ou ocupadas por montanhas. A partir daí identifica **cadeias de montanhas**, **vales** e conexões entre interseções.

```text
   A B C D E
 4 . . . . .  4
 3 X . X . .  3
 2 X X . . .  2
 1 X . . . .  1
   A B C D E
```

Este território tem 5 montanhas em 2 cadeias, e os vales ocupam 6 interseções.

## Representação dos dados

Um **território** é um tuplo de tuplos: um tuplo por caminho vertical, com `0` para interseção livre e `1` para montanha. Uma **interseção** é um tuplo `(letra, número)`, por exemplo `('B', 3)`.

```python
t = ((1, 1, 1, 0),   # caminho vertical 'A'
     (0, 1, 0, 0),   # caminho vertical 'B'
     (0, 0, 1, 0),   # caminho vertical 'C'
     (0, 0, 0, 0),   # caminho vertical 'D'
     (0, 0, 0, 0))   # caminho vertical 'E'
```

## Como executar

Só precisas de Python 3 — o projeto não tem dependências.

```bash
python3 -i FP2324P1.py
```

```python
>>> t = ((1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))
>>> print(territorio_para_str(t))
   A B C D E
 4 . . . . .  4
 3 X . X . .  3
 2 X X . . .  2
 1 X . . . .  1
   A B C D E

>>> obtem_cadeia(t, ('A', 2))
(('A', 1), ('A', 2), ('B', 2), ('A', 3))
>>> obtem_vale(t, ('A', 1))
(('B', 1), ('C', 2), ('B', 3), ('A', 4))
>>> verifica_conexao(t, ('A', 1), ('C', 3))
False
>>> calcula_numero_cadeias_montanhas(t)
2
>>> calcula_tamanho_vales(t)
6
```

## Funções

| Função | Descrição |
| --- | --- |
| `eh_territorio(arg)` | Verifica se o argumento é um território válido. |
| `obtem_ultima_intersecao(t)` | Interseção do extremo superior direito. |
| `eh_intersecao(arg)` | Verifica se o argumento é uma interseção válida. |
| `eh_intersecao_valida(t, i)` | Verifica se a interseção pertence ao território. |
| `eh_intersecao_livre(t, i)` | Verifica se a interseção não tem montanha. |
| `obtem_intersecoes_adjacentes(t, i)` | Interseções adjacentes, por ordem de leitura. |
| `ordena_intersecoes(tup)` | Ordena interseções pela ordem de leitura. |
| `territorio_para_str(t)` | Representação externa do território. |
| `obtem_cadeia(t, i)` | Cadeia a que a interseção pertence. |
| `obtem_vale(t, i)` | Vale da cadeia de montanhas da interseção. |
| `verifica_conexao(t, i1, i2)` | Indica se duas interseções estão conetadas. |
| `calcula_numero_montanhas(t)` | Número de montanhas. |
| `calcula_numero_cadeias_montanhas(t)` | Número de cadeias de montanhas. |
| `calcula_tamanho_vales(t)` | Total de interseções distintas em vales. |

A ordem de leitura de um território é sempre da esquerda para a direita, seguida de baixo para cima.

## Ficheiros

- `FP2324P1.py` — solução completa (ficheiro único, apenas built-ins do Python 3)
- `FP2324P1.md` — enunciado do projeto

---

Autor: João Trigueiros Ferreira (`ist1110573`).
