"""
PQ-Swarm BFT consensus algorithm (simplified model).
"""

import time
import math
from enum import Enum
from typing import Dict, Any

from .crypto import sign_msg, verify_msg


class Phase(Enum):
    IDLE = 0
    PRE_PREPARE = 1
    PREPARE = 2
    COMMIT = 3


class PQSwarmBFT:
    def __init__(self, node_id: str, pubkeys: Dict[str, bytes], sk_sig: bytes, f: int = 1):
        self.node_id = node_id
        self.pubkeys = pubkeys
        self.sk_sig = sk_sig
        self.f = f
        self.phase = Phase.IDLE
        self.current_view = 0
        self.digest = None
        self.start_ts = None
        self.weights = {nid: 1.0 for nid in pubkeys}  # trust weights

    def propose(self, payload: bytes) -> None:
        """Primary node proposes a message."""
        if self.phase != Phase.IDLE:
            return
        self.digest = payload
        self.start_ts = time.time()
        msg = self._make_msg("PRE-PREPARE", payload)
        self.phase = Phase.PRE_PREPARE
        self._broadcast(msg)

    def receive(self, msg: Dict[str, Any]) -> None:
        """Handle incoming message from another node."""
        phase = msg["phase"]
        sender = msg["sender"]

        if not verify_msg(msg["payload"], msg["sig"], self.pubkeys[sender]):
            return

        latency = time.time() - msg["ts"]
        self._update_weight(sender, latency)

        if phase == "PRE-PREPARE" and self.phase == Phase.IDLE:
            self.digest = msg["payload"]
            self.phase = Phase.PREPARE
            self._broadcast(self._make_msg("PREPARE", self.digest))

        elif phase == "PREPARE" and self.phase == Phase.PREPARE:
            self._maybe_commit(msg)

        elif phase == "COMMIT" and self.phase == Phase.COMMIT:
            self._maybe_apply(msg)

    def _make_msg(self, phase: str, payload: bytes) -> Dict[str, Any]:
        return {
            "phase": phase,
            "payload": payload,
            "sender": self.node_id,
            "view": self.current_view,
            "ts": time.time(),
            "sig": sign_msg(payload, self.sk_sig)
        }

    def _broadcast(self, msg):
        print(f"[BROADCAST] {self.node_id} → {msg['phase']}")
        # TODO: implement real networking here

    def _update_weight(self, nid, latency):
        decay = math.exp(-latency)
        self.weights[nid] = 0.8 * self.weights[nid] + 0.2 * decay

    def _maybe_commit(self, msg):
        quorum = sum(self.weights.values())
        threshold = 2 * self.f + 1
        if quorum >= threshold:
            self.phase = Phase.COMMIT
            self._broadcast(self._make_msg("COMMIT", self.digest))

    def _maybe_apply(self, msg):
        print(f"[{self.node_id}] COMMITTED: {self.digest.hex()[:16]}...")
        self.phase = Phase.IDLE
