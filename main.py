from network import P2PNetwork

rede = P2PNetwork()

rede.load_config("exemplo.yaml")

print("Rede válida?", rede.validate())

print("\nFlooding")
print(
    rede.search(
        "n1",
        "r5",
        ttl=5,
        algo="flooding"
    )
)

print("\nRandom Walk")
print(
    rede.search(
        "n1",
        "r5",
        ttl=10,
        algo="random_walk"
    )
)

print("\nInformed Flooding (1ª busca)")
print(
    rede.search(
        "n1",
        "r5",
        ttl=5,
        algo="informed_flooding"
    )
)

print("\nInformed Flooding (2ª busca)")
print(
    rede.search(
        "n1",
        "r5",
        ttl=5,
        algo="informed_flooding"
    )
)

print("\nCache de n1")
print(rede.nodes["n1"].cache)