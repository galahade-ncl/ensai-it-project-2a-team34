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
    """
    Hash a password using the SHA-256 algorithm.

    Parameters
    ----------
    password : str
        Plain text password to hash.
    salt : str, optional
        String added to the password before hashing to protect against
        rainbow table attacks.

    Returns
    -------
    str
        Resulting hexadecimal hash string.
    """
    password_bytes = password.encode("utf-8") + salt.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


def verify_token(x_auth_token=Header(None)) -> UserDao:
    """
    Verify the authenticity of a user via the provided auth token.

    Checks that a token is present in the request headers and validates
    it against the database.

    Parameters
    ----------
    x_auth_token : str, optional
        Token extracted from the ``X-Auth-Token`` HTTP header.

    Returns
    -------
    User
        User associated with the valid token.

    Raises
    ------
    HTTPException
        401 error if the token is missing or not found in the database.
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
    Generate a new secret HMAC key.

    Returns
    -------
    bytes
        New random secret key of 32 bytes.
    """
    return secrets.token_bytes(32)


def encode_secret_key(key: bytes | str) -> str:
    """
    Encode a binary secret key as a Base64 string.

    Parameters
    ----------
    key : bytes or str
        Key to convert. A ``str`` is returned unchanged.

    Returns
    -------
    str
        Base64 representation of the key.
    """
    if isinstance(key, bytes):
        return base64.b64encode(key).decode("ascii")
    return key


def generate_signature(
    secret: bytes, project_id_bytes: bytes, code: bytes, dependency: bytes
) -> bytes:
    """
    Generate the HMAC-SHA256 signature of a project submission.

    Each element is prefixed with its length, so that the boundaries
    between the elements cannot be shifted.

    Parameters
    ----------
    secret : bytes
        Secret HMAC key of the project.
    project_id_bytes : bytes
        Identifier of the project, encoded in UTF-8.
    code : bytes
        Content of the code file.
    dependency : bytes
        Content of the dependency file.

    Returns
    -------
    bytes
        Signature associated with the secret and the files.
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
    """
    Load the application's private signing key from the environment.

    The key is read from ``CERT_SIGNING_PRIVATE_KEY`` and cached.

    Returns
    -------
    Ed25519PrivateKey
        Private signing key of the application.

    Raises
    ------
    RuntimeError
        If ``CERT_SIGNING_PRIVATE_KEY`` is missing.
    """
    pem = os.environ.get("CERT_SIGNING_PRIVATE_KEY")
    if not pem:
        raise RuntimeError(
            "CERT_SIGNING_PRIVATE_KEY is missing: generate a key pair and "
            "set it in the environment."
        )
    return serialization.load_pem_private_key(pem.replace("\\n", "\n").encode(), password=None)


def get_public_key_pem() -> str:
    """
    Return the public key in PEM format, safe to expose.

    Returns
    -------
    str
        Public key in PEM format.
    """
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
    """
    Return the fingerprint of the public key, used as ``kid`` in certificates.

    Returns
    -------
    str
        First 16 hexadecimal characters of the SHA-256 of the public key.
    """
    raw = (
        load_signing_key()
        .public_key()
        .public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    )
    return hashlib.sha256(raw).hexdigest()[:16]


def canonical_json(payload: dict) -> bytes:
    """
    Serialize a payload deterministically, as required for stable signatures.

    Parameters
    ----------
    payload : dict
        Data to serialize.

    Returns
    -------
    bytes
        JSON with sorted keys and no spaces, encoded in UTF-8.
    """
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
