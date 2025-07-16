"""
Stub version of crypto module: no real encryption, just for simulation and testing.
"""

def generate_keys():
    """Stub: generate fake Kyber public/secret keys."""
    return b"kyber_pk", b"kyber_sk"

def encap(peer_pk):
    """Stub: simulate key encapsulation."""
    return b"fake_ciphertext", b"shared_secret"

def decap(ciphertext, sk):
    """Stub: simulate key decapsulation."""
    return b"shared_secret"

def generate_sig_keys():
    """Stub: generate fake Dilithium public/secret keys."""
    return b"dilithium_pk", b"dilithium_sk"

def sign_msg(message, sk):
    """Stub: return fake signature."""
    return b"signature"

def verify_msg(message, signature, pk):
    """Stub: always return True for signature verification."""
    return True
