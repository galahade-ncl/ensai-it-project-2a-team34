import base64
import hashlib
import hmac
import json
import os
import secrets
from functools import lru_cache

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi import Header, HTTPException

from dao.user_dao import UserDao

# --------------
# User Part
# --------------


def hash_password(password: str, salt: str = "") -> str:
    """Hashes a password using the SHA-256 algorithm.
    Args:
        password (str): The plain text password to be hashed.
        salt (str, optional): A string added to the password before hashing
            to protect against rainbow table attacks.
    Returns:
        str: The resulting hexadecimal hash string.
    """
    password_bytes = password.encode("utf-8") + salt.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


# fonction hashage clé HMAC <-> signature -> à faire


def verify_token(x_auth_token=Header(None)) -> UserDao:
    """Verifies the authenticity of a user via the provided auth token.

    This function checks if a token is present in the request headers and
    validates it against the database.
    Args:
        x_auth_token (str, optional): The token extracted from the
            'X-Auth-Token' HTTP header. Defaults to None.
    Returns:
        User object associated with the valid token.
    Raises:
        HTTPException: 401 error if the token is missing.
        HTTPException: 401 error if the token is not found in the database.
    """
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing token.")

    user = UserDao().find_by_token(x_auth_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token.")

    return user


# ------------------
# Project Part
# ------------------


def generate_secret_HMAC_key() -> bytes:
    """
    Generate a new secret key
    Returns:
        New secret key (bytes object)
    """
    return secrets.token_bytes(32)


def encode_secret_key(key: bytes | str) -> str:
    """
    Encode a binary secret key as a Base64 string.
    Args:
        key (bytes | str): key to convert into str
    Return:
        A str representation of the key"""
    if isinstance(key, bytes):
        return base64.b64encode(key).decode("ascii")
    return key


def generate_signature(
    secret: bytes, project_id_bytes: bytes, code: bytes, dependency: bytes
) -> bytes:
    """
    Generate a new signature
    Args:
        secret (str): A secret key
        code (bytes): The binary version of a codefile
        dependency (bytes): The binary version of a dependencyfile
    Returns:
        Signature associated with the secret and the files (bytes object)
    """
    hmac_key = hmac.new(secret, digestmod=hashlib.sha256)

    hmac_key.update(len(project_id_bytes).to_bytes(8, "big"))
    hmac_key.update(project_id_bytes)

    hmac_key.update(len(code).to_bytes(8, "big"))
    hmac_key.update(code)

    hmac_key.update(len(dependency).to_bytes(8, "big"))
    hmac_key.update(dependency)

    return hmac_key.digest()


# --------------------
# Certificate Part
# --------------------


@lru_cache(maxsize=1)
def load_signing_key() -> Ed25519PrivateKey:
    """Loads the application's private signing key from the environment."""
    pem = os.environ.get("CERT_SIGNING_PRIVATE_KEY")
    if not pem:
        raise RuntimeError(
            "CERT_SIGNING_PRIVATE_KEY is missing: generate a key pair and "
            "set it in the environment."
        )
    return serialization.load_pem_private_key(pem.replace("\\n", "\n").encode(), password=None)


def get_public_key_pem() -> str:
    """Returns the public key (PEM), safe to expose."""
    return (
        load_signing_key()
        .public_key()
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode()
    )


def get_key_id() -> str:
    """Fingerprint of the public key, used as 'kid' in certificates."""
    raw = (
        load_signing_key()
        .public_key()
        .public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    )
    return hashlib.sha256(raw).hexdigest()[:16]


def canonical_json(payload: dict) -> bytes:
    """Deterministic serialization, required for stable signatures."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
