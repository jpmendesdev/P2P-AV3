from network import P2PNetwork

rede = P2PNetwork()
rede.load_config("exemplo.yaml")

print("Rede válida?", rede.validate())

print("\nFlooding:")
print(rede.flooding("n1", "r5", ttl=5))

print("\nRandom Walk:")
print(rede.random_walk("n1", "r5", ttl=10))