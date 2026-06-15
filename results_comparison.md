# Resultados dos Testes Comparativos

Este relatório apresenta a comparação entre os algoritmos de busca nas diferentes topologias, considerando o estado do **Cache Frio** (busca sem histórico) e **Cache Quente** (busca após o recurso ter sido localizado e o caminho cacheado).

## Topologia: Ring (Anel)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 12 | 8 | 100% | 12 | 8 | 100% |
| `informed_flooding` | 12 | 8 | 100% | 12 | 8 | 100% |
| `random_walk` | 10.7 | 6.3 | 100% | 11 | 6.5 | 100% |
| `informed_random_walk` | 10.1 | 6.0 | 100% | 11.6 | 6.8 | 100% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 4 | 3 | 100% | 4 | 3 | 100% |
| `informed_flooding` | 4 | 3 | 100% | 4 | 3 | 100% |
| `random_walk` | 11 | 6.5 | 100% | 8.3 | 5.2 | 100% |
| `informed_random_walk` | 11 | 6.5 | 100% | 7.4 | 4.7 | 100% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 10 | 11 | 0% | 10 | 11 | 0% |
| `informed_flooding` | 10 | 11 | 0% | 10 | 11 | 0% |
| `random_walk` | 6 | 7 | 0% | 6 | 7 | 0% |
| `informed_random_walk` | 6 | 7 | 0% | 6 | 7 | 0% |

## Topologia: Mesh (Malha)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 8 | 4 | 100% | 8 | 4 | 100% |
| `informed_flooding` | 8 | 4 | 100% | 8 | 4 | 100% |
| `random_walk` | 10.1 | 6.0 | 90% | 9.6 | 5.6 | 95% |
| `informed_random_walk` | 8.6 | 5.5 | 80% | 6.7 | 4.6 | 85% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 27 | 12 | 100% | 27 | 12 | 100% |
| `informed_flooding` | 27 | 12 | 100% | 27 | 12 | 100% |
| `random_walk` | 13.1 | 7.5 | 70% | 12.8 | 7.8 | 55% |
| `informed_random_walk` | 12.4 | 7.8 | 55% | 12.1 | 7.6 | 55% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 22 | 12 | 0% | 22 | 12 | 0% |
| `informed_flooding` | 22 | 12 | 0% | 22 | 12 | 0% |
| `random_walk` | 6 | 6.5 | 0% | 6 | 6.5 | 0% |
| `informed_random_walk` | 6 | 6.2 | 0% | 6 | 6.4 | 0% |

## Topologia: Scale-Free (Hierárquica)

### Busca por `r6` (Recurso n°6 (Existente, Médio)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 7 | 3 | 100% | 7 | 3 | 100% |
| `informed_flooding` | 7 | 3 | 100% | 7 | 3 | 100% |
| `random_walk` | 10.1 | 7.0 | 45% | 9.1 | 6.4 | 55% |
| `informed_random_walk` | 6.9 | 4.8 | 70% | 7.8 | 6.0 | 65% |

### Busca por `r12` (Recurso n°12 (Existente, Distante)) a partir de `n1` com TTL=10

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 25 | 12 | 100% | 25 | 12 | 100% |
| `informed_flooding` | 25 | 12 | 100% | 25 | 12 | 100% |
| `random_walk` | 11.3 | 7.0 | 55% | 11.2 | 7.1 | 55% |
| `informed_random_walk` | 12.2 | 7.5 | 55% | 10.3 | 6 | 70% |

### Busca por `r99` (Recurso Inexistente (Insucesso)) a partir de `n1` com TTL=5

| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |
| --- | --- | --- | --- | --- | --- | --- |
| `flooding` | 23 | 12 | 0% | 23 | 12 | 0% |
| `informed_flooding` | 23 | 12 | 0% | 23 | 12 | 0% |
| `random_walk` | 6 | 6.1 | 0% | 6 | 6.2 | 0% |
| `informed_random_walk` | 6 | 6.5 | 0% | 6 | 6.2 | 0% |

