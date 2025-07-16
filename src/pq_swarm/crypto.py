"""
Post-quantum crypto helpers using pqcrypto:
- Kyber-1024 (KEM)
- Dilithium-5 (Signature)
"""

from pqcrypto.kem.kyber_1024 import generate_keypair as kyber_keypair
from pqcrypto.kem.kyber_1024 import encrypt as kyber_encap
from pqcrypto.kem.kyber_1024 import decrypt as kyber_decap

from pqcrypto.sign.dilithium5 import generate_keypair as dilithium_keypair
from pqcrypto.sign.dilithium5 import sign as dilithium_sign
from pqcrypto.sign.dilithium5 import verify as dilithium_verify

# ---------------------- KYBER-1024 ----------------------

def generate_keys():
    """Generate Kyber public/secret key pair."""
    pk, sk = kyber_keypair()
    return pk, sk

def encap(peer_pk: bytes):
    """Encapsulate a shared secret for peer's public key."""
    ct, ss = kyber_encap(peer_pk)
    return ct, ss

def decap(ct: bytes, sk: bytes):
    """Decapsulate ciphertext to shared secret."""
    return kyber_decap(ct, sk)

# ---------------------- DILITHIUM-5 ---------------------

def generate_sig_keys():
    """Generate Dilithium public/secret key pair."""
    pk, sk = dilithium_keypair()
    return pk, sk

def sign_msg(msg: bytes, sk: bytes):
    """Sign message using Dilithium private key."""
    return dilithium_sign(msg, sk)

def verify_msg(msg: bytes, sig: bytes, pk: bytes) -> bool:
    """Verify message signature using public key."""
    try:
        dilithium_verify(msg, sig, pk)
        return True
    except Exception:
        return False
