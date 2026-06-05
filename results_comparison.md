# Resultados dos Testes Comparativos

Este relatório apresenta a comparação entre os algoritmos de busca nas diferentes topologias, considerando o estado do **Cache Frio** (busca sem histórico) e **Cache Quente** (busca após o recurso ter sido localizado e o caminho cacheado).

## Topologia: Ring (Anel)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 12 | 8 | 100% | 12 | 8 | 100% |
| `informed_flooding` | 12 | 8 | 100% | 8 | 5 | 100% |
| `random_walk` | 10.7 | 6.3 | 100% | 11 | 6.5 | 100% |
| `informed_random_walk` | 10.1 | 6.0 | 100% | 8 | 5 | 100% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 4 | 3 | 100% | 4 | 3 | 100% |
| `informed_flooding` | 4 | 3 | 100% | 2 | 2 | 100% |
| `random_walk` | 11.9 | 7.0 | 100% | 12.8 | 7.4 | 100% |
| `informed_random_walk` | 8.3 | 5.2 | 100% | 2 | 2 | 100% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 10 | 11 | 0% | 10 | 11 | 0% |
| `informed_flooding` | 10 | 11 | 0% | 10 | 11 | 0% |
| `random_walk` | 5 | 6 | 0% | 5 | 6 | 0% |
| `informed_random_walk` | 5 | 6 | 0% | 5 | 6 | 0% |

## Topologia: Mesh (Malha)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 10 | 5 | 100% | 10 | 5 | 100% |
| `informed_flooding` | 10 | 5 | 100% | 4 | 3 | 100% |
| `random_walk` | 7.5 | 5.3 | 75% | 7 | 4.7 | 90% |
| `informed_random_walk` | 7.6 | 4.9 | 90% | 4 | 3 | 100% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 27 | 12 | 100% | 27 | 12 | 100% |
| `informed_flooding` | 27 | 12 | 100% | 10 | 6 | 100% |
| `random_walk` | 12.4 | 7.2 | 55% | 11.4 | 7.3 | 45% |
| `informed_random_walk` | 11 | 7.5 | 50% | 10 | 6 | 100% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 22 | 12 | 0% | 22 | 12 | 0% |
| `informed_flooding` | 22 | 12 | 0% | 22 | 12 | 0% |
| `random_walk` | 5 | 5.7 | 0% | 5 | 5.8 | 0% |
| `informed_random_walk` | 5 | 5.6 | 0% | 5 | 5.8 | 0% |

## Topologia: Scale-Free (Hierárquica)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 7 | 3 | 100% | 7 | 3 | 100% |
| `informed_flooding` | 7 | 3 | 100% | 2 | 2 | 100% |
| `random_walk` | 10.9 | 6.8 | 60% | 9 | 5.7 | 70% |
| `informed_random_walk` | 10.3 | 6.7 | 60% | 2 | 2 | 100% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 25 | 12 | 100% | 25 | 12 | 100% |
| `informed_flooding` | 25 | 12 | 100% | 6 | 4 | 100% |
| `random_walk` | 9.3 | 6.8 | 40% | 10.7 | 6.5 | 50% |
| `informed_random_walk` | 9.2 | 6.5 | 50% | 6 | 4 | 100% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 23 | 12 | 0% | 23 | 12 | 0% |
| `informed_flooding` | 23 | 12 | 0% | 23 | 12 | 0% |
| `random_walk` | 5 | 5.7 | 0% | 5 | 5.4 | 0% |
| `informed_random_walk` | 5 | 5.9 | 0% | 5 | 5.5 | 0% |

