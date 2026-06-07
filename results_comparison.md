# Resultados dos Testes Comparativos

Este relatório apresenta a comparação entre os algoritmos de busca nas diferentes topologias, considerando o estado do **Cache Frio** (busca sem histórico) e **Cache Quente** (busca após o recurso ter sido localizado e o caminho cacheado).

## Topologia: Ring (Anel)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 13 | 9 | 100% | 13 | 9 | 100% |
| `informed_flooding` | 13 | 9 | 100% | 8 | 5 | 100% |
| `random_walk` | 11.3 | 6.7 | 100% | 12.2 | 7.1 | 100% |
| `informed_random_walk` | 11.6 | 6.8 | 100% | 8 | 5 | 100% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 3 | 2 | 100% | 3 | 2 | 100% |
| `informed_flooding` | 3 | 2 | 100% | 2 | 2 | 100% |
| `random_walk` | 12.8 | 7.4 | 100% | 11 | 6.5 | 100% |
| `informed_random_walk` | 11.9 | 7.0 | 100% | 2 | 2 | 100% |

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
| `random_walk` | 7.5 | 4.8 | 95% | 6.5 | 4.3 | 95% |
| `informed_random_walk` | 8.2 | 5.5 | 80% | 4 | 3 | 100% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 27 | 12 | 100% | 27 | 12 | 100% |
| `informed_flooding` | 27 | 12 | 100% | 10 | 6 | 100% |
| `random_walk` | 10.8 | 7.6 | 35% | 11 | 7.7 | 30% |
| `informed_random_walk` | 11.2 | 6.7 | 50% | 10 | 6 | 100% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 22 | 12 | 0% | 22 | 12 | 0% |
| `informed_flooding` | 22 | 12 | 0% | 22 | 12 | 0% |
| `random_walk` | 5 | 5.7 | 0% | 5 | 5.9 | 0% |
| `informed_random_walk` | 5 | 5.9 | 0% | 5 | 5.9 | 0% |

## Topologia: Scale-Free (Hierárquica)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 11 | 5 | 100% | 11 | 5 | 100% |
| `informed_flooding` | 11 | 5 | 100% | 2 | 2 | 100% |
| `random_walk` | 10.7 | 6.7 | 60% | 6.9 | 4.8 | 70% |
| `informed_random_walk` | 9.4 | 6.8 | 60% | 2 | 2 | 100% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 25 | 12 | 100% | 25 | 12 | 100% |
| `informed_flooding` | 25 | 12 | 100% | 6 | 4 | 100% |
| `random_walk` | 10.7 | 6.9 | 60% | 10.1 | 6.8 | 55% |
| `informed_random_walk` | 12.1 | 7.0 | 55% | 6 | 4 | 100% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 23 | 12 | 0% | 23 | 12 | 0% |
| `informed_flooding` | 23 | 12 | 0% | 23 | 12 | 0% |
| `random_walk` | 5 | 5.4 | 0% | 5 | 5.7 | 0% |
| `informed_random_walk` | 5 | 5.7 | 0% | 5 | 5.3 | 0% |

