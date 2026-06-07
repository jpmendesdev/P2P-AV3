import os
import sys
from network import P2PNetwork
import run_tests

def print_banner():
    print("=" * 60)
    print("       SIMULADOR DE BUSCA EM REDES P2P NÃO ESTRUTURADAS       ")
    print("=" * 60)

def show_network_info(net):
    print(f"\n[+] Rede Carregada e Validada com Sucesso!")
    print(f"  - Total de nós estabelecido (num_nodes): {net.num_nodes}")
    print(f"  - Nós carregados: {len(net.nodes)}")
    print(f"  - Conectividade mínima de vizinhos (min_neighbors): {net.min_neighbors}")
    print(f"  - Conectividade máxima de vizinhos (max_neighbors): {net.max_neighbors}")
    
    print("\n--- Nós e seus recursos ---")
    for node_id, node in sorted(net.nodes.items(), key=lambda x: int(x[0].replace("n", "")) if x[0].replace("n", "").isdigit() else x[0]):
        vizinhos_str = ", ".join(sorted(node.neighbors))
        recursos_str = ", ".join(sorted(node.resources))
        print(f"  Nó {node_id} ({len(node.neighbors)} vizinhos: [{vizinhos_str}]) -> Recursos: [{recursos_str}]")
    print("-" * 60)

def menu():
    print("\nMenu de Operações:")
    print("1. Realizar Busca Individual por Recurso")
    print("2. Visualizar Caches de Roteamento")
    print("3. Limpar Todos os Caches")
    print("4. Executar Bateria de Testes Comparativos")
    print("5. Carregar outro arquivo de configuração")
    print("6. Sair")
    
    choice = input("\nEscolha uma opção (1-6): ").strip()
    return choice

def run_individual_search(net):
    print("\n--- Execução de Busca ---")
    
    # Input node_id
    node_id = input(f"Digite o identificador do nó de origem (ex: n1): ").strip()
    if node_id not in net.nodes:
        print(f"[-] Erro: O nó '{node_id}' não existe na rede.")
        return

    # Input resource_id
    resource_id = input("Digite o identificador do recurso a ser buscado (ex: r5): ").strip()
    if not resource_id:
        print("[-] Erro: O identificador do recurso não pode ser vazio.")
        return

    # Input TTL
    ttl_str = input("Digite o valor do TTL da busca (ex: 5): ").strip()
    if not ttl_str.isdigit():
        print("[-] Erro: O TTL deve ser um número inteiro positivo.")
        return
    ttl = int(ttl_str)

    # Input Algo
    print("\nAlgoritmos disponíveis:")
    print("1. flooding (Inundação Cega)")
    print("2. informed_flooding (Inundação Informada por Cache)")
    print("3. random_walk (Passeio Aleatório)")
    print("4. informed_random_walk (Passeio Aleatório Informado por Cache)")
    
    algo_choice = input("Escolha o algoritmo (1-4): ").strip()
    
    algo_map = {
        "1": "flooding",
        "2": "informed_flooding",
        "3": "random_walk",
        "4": "informed_random_walk"
    }
    
    if algo_choice not in algo_map:
        print("[-] Erro: Opção de algoritmo inválida.")
        return
        
    algo = algo_map[algo_choice]
    
    print(f"\n[i] Iniciando busca pelo recurso '{resource_id}' a partir de '{node_id}' usando '{algo}' (TTL={ttl})...")
    
    try:
        res = getattr(net, algo)(node_id, resource_id, ttl)
        
        print("\n" + "=" * 40)
        print("            RESULTADOS DA BUSCA            ")
        print("=" * 40)
        if res["found"]:
            print(f"[+] Sucesso: Recurso ENCONTRADO!")
            print(f"  - Nó Proprietário: {res['owner']}")
            path_str = " -> ".join(res["path"])
            print(f"  - Caminho de Busca: {path_str}")
        else:
            print(f"[-] Insucesso: Recurso NÃO encontrado (TTL expirou ou rede percorrida).")
            
        print(f"  - Mensagens Trocadas: {res['messages']}")
        print(f"  - Nós Envolvidos: {res['nodes_involved']}")
        print("=" * 40)
        
        # Display cache updates
        if res["found"] and len(res["path"]) > 1:
            print("[i] Os caches dos nós intermediários foram atualizados com a rota de resposta.")
            
    except Exception as e:
        print(f"[-] Ocorreu um erro ao executar a busca: {e}")

def show_caches(net):
    print("\n--- Caches de Roteamento Locais ---")
    has_cache = False
    for node_id, node in sorted(net.nodes.items(), key=lambda x: int(x[0].replace("n", "")) if x[0].replace("n", "").isdigit() else x[0]):
        if node.cache:
            has_cache = True
            cache_details = ", ".join([f"'{res}': vai para '{neighbor}'" for res, neighbor in node.cache.items()])
            print(f"  Nó {node_id} cache -> {{{cache_details}}}")
            
    if not has_cache:
        print("  [i] Todos os caches estão atualmente vazios.")
    print("-" * 40)

def clear_all_caches(net):
    run_tests.clear_caches(net)
    print("\n[+] Todos os caches dos nós foram limpos com sucesso!")

def load_and_validate_network():
    while True:
        filename = input("\nDigite o caminho do arquivo de configuração (YAML/JSON) [Pressione Enter para 'exemplo.yaml']: ").strip()
        if not filename:
            filename = "exemplo.yaml"
            
        if not os.path.exists(filename):
            print(f"[-] Erro: Arquivo '{filename}' não encontrado.")
            retry = input("Deseja tentar novamente? (s/n): ").strip().lower()
            if retry != 's':
                return None
            continue
            
        print(f"[i] Carregando e validando '{filename}'...")
        net = P2PNetwork()
        try:
            net.load_config(filename)
            net.validate()
            return net
        except Exception as e:
            print(f"\n[!] A REDE É INVÁLIDA! Falha na Validação:")
            print(f"    Erro: {e}")
            retry = input("\nDeseja carregar outro arquivo? (s/n): ").strip().lower()
            if retry != 's':
                return None

def main():
    print_banner()
    net = load_and_validate_network()
    
    if not net:
        print("\nSaindo do simulador. Até logo!")
        sys.exit(0)
        
    show_network_info(net)
    
    while True:
        choice = menu()
        
        if choice == "1":
            run_individual_search(net)
        elif choice == "2":
            show_caches(net)
        elif choice == "3":
            clear_all_caches(net)
        elif choice == "4":
            print("\n[i] Iniciando suite de testes automatizada nas topologias Ring, Mesh e Scale-Free...")
            try:
                run_tests.main()
            except Exception as e:
                print(f"[-] Erro ao executar testes: {e}")
        elif choice == "5":
            new_net = load_and_validate_network()
            if new_net:
                net = new_net
                show_network_info(net)
        elif choice == "6":
            print("\nSaindo do simulador. Até logo!")
            break
        else:
            print("[-] Opção inválida. Escolha um número de 1 a 6.")

if __name__ == "__main__":
    main()
