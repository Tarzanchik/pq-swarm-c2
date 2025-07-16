"""
Toy simulation with 20 swarm nodes running PQ-Swarm BFT.
"""

import time
from pq_swarm.node import Node

# Создаём 20 узлов
nodes = [Node(f"n{i}") for i in range(20)]

# Полносвязная топология (все соединены со всеми)
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        nodes[i].connect(nodes[j])

# Инициализируем консенсус для всех узлов
for node in nodes:
    node.init_consensus(f=3)  # допускаем до 3 скомпрометированных узлов

# Узел n0 инициирует команду
leader = nodes[0]
leader.broadcast_command(b"COMMAND: INTERCEPT TARGET XYZ")

# Даём время на консенсус (в имитации)
time.sleep(2)
