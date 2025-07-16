"""
Swarm node abstraction for PQ-Swarm C2
"""

from typing import Dict
from . import crypto
from .consensus import PQSwarmBFT


class Node:
    def __init__(self, node_id: str):
        self.node_id = node_id

        # Key pairs
        self.pk_kem, self.sk_kem = crypto.generate_keys()
        self.pk_sig, self.sk_sig = crypto.generate_sig_keys()

        # Peers and consensus
        self.peers: Dict[str, Node] = {}
        self.consensus = None

    def connect(self, peer: 'Node'):
        """Mutual connection (bidirectional link)."""
        self.peers[peer.node_id] = peer
        peer.peers[self.node_id] = self

    def init_consensus(self, f: int = 1):
        """Initialize BFT consensus with peers' public keys."""
        pubkeys = {nid: n.pk_sig for nid, n in self.peers.items()}
        pubkeys[self.node_id] = self.pk_sig
        self.consensus = PQSwarmBFT(self.node_id, pubkeys, self.sk_sig, f=f)

    def broadcast_command(self, command: bytes):
        """Send command into the swarm consensus."""
        if not self.consensus:
            raise RuntimeError("Consensus not initialized")
        self.consensus.propose(command)
