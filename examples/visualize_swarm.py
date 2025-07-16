"""
Visualize a swarm graph with 20 nodes using networkx and matplotlib.
"""

import networkx as nx
import matplotlib.pyplot as plt
from pq_swarm.node import Node

# создаём 20 узлов
nodes = [Node(f"n{i}") for i in range(20)]

# создаём пустой граф
G = nx.Graph()

# добавляем узлы
for n in nodes:
    G.add_node(n.node_id)

# соединяем всех со всеми (полносвязная топология)
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        nodes[i].connect(nodes[j])
        G.add_edge(nodes[i].node_id, nodes[j].node_id)

# рисуем
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", edge_color="gray")
plt.title("PQ-Swarm C2 — Swarm Topology")
plt.tight_layout()
plt.show()
