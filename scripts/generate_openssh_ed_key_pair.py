from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def generate_ed25519_key_pair() -> None:
    """
    Generate a private/public key pair for Ed25519 signature algorithm.
    """
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    )

    with open("openssh_ed25519_private_key.pem", "wb") as f:
        f.write(private_pem)

    with open("openssh_ed25519_public_key.pem", "wb") as f:
        f.write(public_pem)

    print(
        "Private key saved to: ed25519_private_key.pem",
        "Public key saved to: ed25519_public_key.pem",
    )


if __name__ == "__main__":
    generate_ed25519_key_pair()
