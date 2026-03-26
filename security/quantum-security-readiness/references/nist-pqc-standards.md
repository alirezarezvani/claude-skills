# NIST PQC Standards — Algorithm Reference

NIST completed PQC standardization with FIPS 203, 204, and 205 published in August 2024.

## Key Encapsulation Mechanism (KEM)

### CRYSTALS-Kyber (FIPS 203 — ML-KEM)

Kyber is based on the Module Learning With Errors (MLWE) problem. It is the primary replacement for RSA and ECDH key exchange.

Security parameter sets:
- ML-KEM-512: ~128 bits classical security (not recommended for new systems)
- ML-KEM-768: ~192 bits classical security (recommended general purpose)
- ML-KEM-1024: ~256 bits classical security (required for data > 10 year sensitivity)

Performance: Kyber key generation and encapsulation are faster than RSA-2048 key exchange in most benchmark environments. Public key sizes are larger (1184 bytes for ML-KEM-768 vs 256 bytes for P-256 public key) — protocol designers must account for this in handshake buffers and certificate infrastructure.

## Digital Signatures

### CRYSTALS-Dilithium (FIPS 204 — ML-DSA)

Dilithium is the primary replacement for RSA-PSS and ECDSA in code signing, TLS certificates, and document signing. Based on Module Learning With Errors.

Security parameter sets:
- ML-DSA-44: ~128 bits security
- ML-DSA-65: ~192 bits security (recommended)
- ML-DSA-87: ~256 bits security

### SPHINCS+ (FIPS 205 — SLH-DSA)

Hash-based signature scheme. Conservative fallback — security depends only on hash function security, not on unproven lattice problem assumptions. Larger signatures and slower performance than Dilithium. Recommended for firmware signing where signature generation is infrequent but long-term trust is critical.

### FALCON (FIPS 206 — FN-DSA)

NTRU lattice-based signatures. Compact signature sizes, useful for constrained environments. Requires side-channel-resistant implementation.

---

## Hybrid Classical + PQC Transition Approach

During the transition period, hybrid key exchange is the recommended approach. Hybrid schemes combine a classical key exchange (X25519 ECDH) with a PQC KEM (ML-KEM-768) and derive the session key from both shared secrets. This provides:

- Security if PQC algorithms prove weaker than expected
- Security if classical algorithms remain unbroken before CRQC
- Forward compatibility with post-CRQC environments

TLS 1.3 hybrid groups standardized in IETF RFC 9496:
- `X25519MLKEM768` (IANA code point 0x11ec)
- `SecP256r1MLKEM768`
