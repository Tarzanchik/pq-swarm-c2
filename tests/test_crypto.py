"""
Unit tests for crypto module using pytest.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from pq_swarm import crypto

from pq_swarm import crypto


def test_kyber_key_encapsulation():
    """Test Kyber keypair, encapsulation, and decapsulation."""
    pk, sk = crypto.generate_keys()
    ct, ss1 = crypto.encap(pk)
    ss2 = crypto.decap(ct, sk)
    assert ss1 == ss2, "Shared secrets do not match (Kyber KEM)"


def test_dilithium_signature():
    """Test Dilithium signing and verification."""
    pk, sk = crypto.generate_sig_keys()
    message = b"Post-quantum Swarm C2 test"
    sig = crypto.sign_msg(message, sk)
    assert crypto.verify_msg(message, sig, pk), "Dilithium signature verification failed"
