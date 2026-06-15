# Trabalho 7 – Implementação de Algoritmos de Busca em Sistemas P2P

Disciplina: Computação Distribuída  
Professor: Nabor C. Mendonça

---

# Integrantes

<h2>Integrantes</h2>

<table>
    <tr>
        <th>Integrante</th>
        <th>Matrícula</th>
    </tr>
    <tr>
        <td>João Pedro Mendes</td>
        <td>2315069</td>
    </tr>
    <tr>
        <td>João Felipe Ribeiro de Melo</td>
        <td>2315045</td>
    </tr>
    <tr>
        <td>Bianca Oriá Leite</td>
        <td>2320323</td>
    </tr>
    <tr>
        <td>Lorenna Aguiar Nunes</td>
        <td>2315026</td>
    </tr>
</table>

# Objetivo

Implementar um simulador de redes P2P não estruturadas capaz de:

- Carregar topologias a partir de arquivos YAML ou JSON;
- Validar a rede conforme os requisitos do trabalho;
- Executar buscas por recursos utilizando diferentes algoritmos;
- Comparar desempenho entre algoritmos e topologias;
- Gerar estatísticas e gráficos de desempenho.

---

# Algoritmos Implementados

## Flooding

A consulta é enviada para todos os vizinhos do nó atual.

Características:

- Alta taxa de sucesso;
- Grande consumo de mensagens;
- Busca semelhante à Busca em Largura (BFS).

---

## Informed Flooding

Versão otimizada do Flooding.

Utiliza cache local para armazenar rotas previamente descobertas.

Benefícios:

- Menor número de mensagens;
- Menor tempo de localização após a primeira busca.

---

## Random Walk

A consulta é enviada para apenas um vizinho escolhido aleatoriamente.

Características:

- Baixo tráfego de rede;
- Menor consumo de mensagens;
- Pode não encontrar o recurso mesmo quando ele existe.

---

## Informed Random Walk

Versão otimizada do Random Walk.

Utiliza cache local para direcionar buscas futuras.

Benefícios:

- Mantém baixo tráfego;
- Aumenta a taxa de sucesso após buscas anteriores.

---

# Estrutura do Projeto

```text
.
├── main.py
├── network.py
├── node.py
├── run_tests.py
│
├── topologies/
│   ├── topo_ring.yaml
│   ├── topo_mesh.yaml
│   └── topo_scale_free.yaml
│
├── graphs/
│   ├── mensagens/
│   ├── nos/
│   └── sucesso/
│
└── results_comparison.md
```

---

# Formato do Arquivo de Entrada

Exemplo:

```yaml
num_nodes: 5

min_neighbors: 1
max_neighbors: 3

resources:
  n1: [r1, r2]
  n2: [r3]
  n3: [r4]
  n4: [r5]
  n5: [r6]

edges:
  - [n1, n2]
  - [n1, n3]
  - [n2, n4]
  - [n3, n5]
```

---

# Executando o Projeto

## Criar ambiente virtual

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

ou

```bash
pip install pyyaml matplotlib networkx
```

---

# Executando o Simulador

```bash
python main.py
```

Menu disponível:

```text
1. Realizar Busca Individual por Recurso
2. Visualizar Caches de Roteamento
3. Limpar Todos os Caches
4. Executar Bateria de Testes Comparativos
5. Carregar outro arquivo de configuração
6. Sair
```

---

# Parâmetros de Busca

Cada busca recebe:

| Parâmetro | Descrição |
|------------|------------|
| node_id | Nó de origem |
| resource_id | Recurso desejado |
| ttl | Número máximo de saltos |
| algo | Algoritmo utilizado |

Exemplo:

```text
Origem: n1
Recurso: r5
TTL: 5
Algoritmo: flooding
```

---

# TTL

TTL (Time To Live) representa o número máximo de saltos permitidos para a consulta.

Exemplo:

```text
TTL = 4

n1 → n2 → n3 → n4 → n5
```

Ao chegar em n5:

```text
TTL = 0
```

A busca ainda pode verificar se o recurso está presente em n5.

Caso seja necessário encaminhar novamente, a busca é encerrada.

---

# Testes Comparativos

A opção:

```text
4. Executar Bateria de Testes Comparativos
```

executa automaticamente testes nas topologias:

- Ring
- Mesh
- Scale-Free

para os recursos:

```text
r6
r12
r99
```

e gera:

```text
results_comparison.md
```

---

# Métricas Avaliadas

## Número de Mensagens

Quantidade total de mensagens trocadas entre os nós.

---

## Nós Envolvidos

Quantidade de nós visitados durante a busca.

---

## Taxa de Sucesso

Percentual de execuções que localizaram o recurso.

---

# Gráficos Gerados

O sistema gera gráficos para:

## Mensagens Trocadas

Comparação entre algoritmos.

## Nós Envolvidos

Impacto da topologia sobre a busca.

## Taxa de Sucesso

Eficiência dos algoritmos.

---

# Topologias Avaliadas

## Ring

Estrutura circular.

Características:

- Poucas conexões;
- Caminhos maiores.

---

## Mesh

Estrutura altamente conectada.

Características:

- Muitos caminhos alternativos;
- Menor distância média.

---

## Scale-Free

Estrutura hierárquica com hubs.

Características:

- Alguns nós possuem muitas conexões;
- Busca tende a ser mais eficiente.

---

# Funcionalidades Extras

Além dos requisitos obrigatórios, o projeto implementa:

- Cache de roteamento;
- Flooding Informado;
- Random Walk Informado;
- Rastreamento detalhado da busca;
- Visualização gráfica da rede carregada;
- Geração automática de gráficos comparativos.

---

# Conclusão

Os testes demonstram o impacto da topologia e do algoritmo de busca sobre:

- número de mensagens;
- número de nós envolvidos;
- taxa de sucesso.

O Flooding apresenta maior taxa de sucesso, porém com maior custo de comunicação.

O Random Walk reduz significativamente o tráfego da rede, mas pode falhar em localizar recursos quando o TTL é limitado.

O uso de cache melhora significativamente o desempenho das buscas subsequentes em ambos os algoritmos.