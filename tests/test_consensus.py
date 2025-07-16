"""
Test for PQSwarmBFT consensus using stubs.
"""

import time
from pq_swarm.consensus import PQSwarmBFT
from pq_swarm.crypto import generate_sig_keys

def test_consensus_phases():
    """Simulate two nodes going through PRE-PREPARE → COMMIT."""
    # Сгенерируем ключи двух участников
    pk1, sk1 = generate_sig_keys()
    pk2, sk2 = generate_sig_keys()

    pubkeys = {"node1": pk1, "node2": pk2}

    # Инициализируем два узла с консенсусом
    node1 = PQSwarmBFT("node1", pubkeys, sk1, f=0)
    node2 = PQSwarmBFT("node2", pubkeys, sk2, f=0)

    # node1 инициирует предложение
    payload = b"command: intercept"
    node1.propose(payload)

    # имитируем отправку сообщения
    msg = node1._make_msg("PRE-PREPARE", payload)
    node2.receive(msg)

    msg2 = node2._make_msg("PREPARE", payload)
    node1.receive(msg2)

    msg3 = node1._make_msg("COMMIT", payload)
    node2.receive(msg3)

    # ДОБАВЛЕНО: ещё один prepare от node1 → node2
    msg4 = node1._make_msg("PREPARE", payload)
    node2.receive(msg4)

    msg5 = node2._make_msg("COMMIT", payload)
    node2.receive(msg5)

    # финальная фаза должна быть IDLE (после COMMIT)
    assert node2.phase.name == "IDLE"
