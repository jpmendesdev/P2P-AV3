import os
import random
from network import P2PNetwork

def clear_caches(net):
    for node in net.nodes.values():
        node.cache.clear()

def run_experiment(topology_file, start_node, resource_id, ttl, runs=20):
    net = P2PNetwork()
    net.load_config(topology_file)
    net.validate()
    
    algorithms = ["flooding", "informed_flooding", "random_walk", "informed_random_walk"]
    results = {}
    
    for algo in algorithms:
        # 1. Cold Cache
        clear_caches(net)
        
        if "random_walk" in algo:
            # Stochastic algorithm: run multiple times and average
            cold_successes = 0
            cold_msg_sum = 0
            cold_nodes_sum = 0
            
            for _ in range(runs):
                clear_caches(net)  # keep it cold
                res = getattr(net, algo)(start_node, resource_id, ttl)
                if res["found"]:
                    cold_successes += 1
                cold_msg_sum += res["messages"]
                cold_nodes_sum += res["nodes_involved"]
                
            cold_found = cold_successes > 0
            cold_msg = cold_msg_sum / runs
            cold_nodes = cold_nodes_sum / runs
            cold_success_rate = cold_successes / runs
        else:
            # Deterministic algorithm
            res = getattr(net, algo)(start_node, resource_id, ttl)
            cold_found = res["found"]
            cold_msg = res["messages"]
            cold_nodes = res["nodes_involved"]
            cold_success_rate = 1.0 if cold_found else 0.0
            
        # 2. Hot Cache
        # For hot cache, we must FIRST run a successful search to populate the cache (if possible)
        clear_caches(net)
        # We run a standard search once (using standard flooding to ensure the path to the resource is cached)
        setup_res = net.flooding(start_node, resource_id, ttl)
        has_cached = setup_res["found"]
        
        if "random_walk" in algo:
            hot_successes = 0
            hot_msg_sum = 0
            hot_nodes_sum = 0
            
            for _ in range(runs):
                # Repopulate cache for each run, since random walks can be stochastic but cache is helper
                clear_caches(net)
                net.flooding(start_node, resource_id, ttl) # repopulate
                res = getattr(net, algo)(start_node, resource_id, ttl)
                if res["found"]:
                    hot_successes += 1
                hot_msg_sum += res["messages"]
                hot_nodes_sum += res["nodes_involved"]
                
            hot_found = hot_successes > 0
            hot_msg = hot_msg_sum / runs
            hot_nodes = hot_nodes_sum / runs
            hot_success_rate = hot_successes / runs
        else:
            # Deterministic
            res = getattr(net, algo)(start_node, resource_id, ttl)
            hot_found = res["found"]
            hot_msg = res["messages"]
            hot_nodes = res["nodes_involved"]
            hot_success_rate = 1.0 if hot_found else 0.0
            
        results[algo] = {
            "cold": {"found": cold_found, "msg": cold_msg, "nodes": cold_nodes, "rate": cold_success_rate},
            "hot": {"found": hot_found, "msg": hot_msg, "nodes": hot_nodes, "rate": hot_success_rate}
        }
        
    return results

def main():
    topologies = {
        "Ring (Anel)": "topologies/topo_ring.yaml",
        "Mesh (Malha)": "topologies/topo_mesh.yaml",
        "Scale-Free (Hierárquica)": "topologies/topo_scale_free.yaml"
    }
    
    # We will search for a resource that exists (e.g. r6, r12) and one that does not exist (r99)
    test_cases = [
        {"resource": "r6", "ttl": 10, "desc": "Recurso n°6 (Existente, Médio)"},
        {"resource": "r12", "ttl": 10, "desc": "Recurso n°12 (Existente, Distante)"},
        {"resource": "r99", "ttl": 5, "desc": "Recurso Inexistente (Insucesso)"}
    ]
    
    start_node = "n1"
    
    markdown_report = "# Resultados dos Testes Comparativos\n\n"
    markdown_report += "Este relatório apresenta a comparação entre os algoritmos de busca nas diferentes topologias, considerando o estado do **Cache Frio** (busca sem histórico) e **Cache Quente** (busca após o recurso ter sido localizado e o caminho cacheado).\n\n"
    
    for topo_name, topo_file in topologies.items():
        markdown_report += f"## Topologia: {topo_name}\n\n"
        
        for case in test_cases:
            res_id = case["resource"]
            ttl = case["ttl"]
            desc = case["desc"]
            
            markdown_report += f"### Busca por `{res_id}` ({desc}) a partir de `{start_node}` com TTL={ttl}\n\n"
            markdown_report += "| Algoritmo | Cache Frio: Msg (Méd.) | Cache Frio: Nós (Méd.) | Cache Frio: Sucesso % | Cache Quente: Msg (Méd.) | Cache Quente: Nós (Méd.) | Cache Quente: Sucesso % |\n"
            markdown_report += "| --- | --- | --- | --- | --- | --- | --- |\n"
            
            results = run_experiment(topo_file, start_node, res_id, ttl)
            
            for algo, data in results.items():
                cold = data["cold"]
                hot = data["hot"]
                
                fmt = lambda x: f"{x:.1f}" if isinstance(x, float) and not x.is_integer() else f"{int(x)}"
                
                c_msg = fmt(cold['msg'])
                c_nds = fmt(cold['nodes'])
                c_rate = f"{cold['rate']*100:.0f}%"
                
                h_msg = fmt(hot['msg'])
                h_nds = fmt(hot['nodes'])
                h_rate = f"{hot['rate']*100:.0f}%"
                
                markdown_report += f"| `{algo}` | {c_msg} | {c_nds} | {c_rate} | {h_msg} | {h_nds} | {h_rate} |\n"
            
            markdown_report += "\n"
            
    print(markdown_report)
    
    # Write to a file
    with open("results_comparison.md", "w", encoding="utf-8") as f:
        f.write(markdown_report)
    print("Relatório salvo em results_comparison.md")

if __name__ == "__main__":
    # Seed random for reproducibility
    random.seed(42)
    main()
