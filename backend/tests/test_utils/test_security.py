import base64
import hashlib
import hmac
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from utils.security import (
    encode_secret_key,
    generate_secret_HMAC_key,
    generate_signature,
    hash_password,
    verify_token,
)


# ---------------------------------------------------------------------------
# hash_password
# ---------------------------------------------------------------------------
class TestHashPassword:
    def test_known_value_without_salt(self):
        expected = hashlib.sha256(b"password").hexdigest()
        assert hash_password("password") == expected

    def test_known_value_with_salt(self):
        expected = hashlib.sha256(b"passwordsalt").hexdigest()
        assert hash_password("password", "salt") == expected

    def test_default_salt_is_empty(self):
        assert hash_password("abc") == hash_password("abc", "")

    def test_is_deterministic(self):
        assert hash_password("abc", "s") == hash_password("abc", "s")

    def test_different_salts_give_different_hashes(self):
        assert hash_password("abc", "s1") != hash_password("abc", "s2")

    def test_different_passwords_give_different_hashes(self):
        assert hash_password("abc") != hash_password("abd")

    def test_output_format(self):
        result = hash_password("abc")
        assert isinstance(result, str)
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_empty_password(self):
        assert hash_password("") == hashlib.sha256(b"").hexdigest()

    def test_unicode_password(self):
        expected = hashlib.sha256("pässwörd🔐".encode()).hexdigest()
        assert hash_password("pässwörd🔐") == expected

    def test_concatenation_is_ambiguous(self):
        """Documente le comportement actuel : password + salt est simplement
        concaténé, donc ("ab", "c") et ("a", "bc") donnent le même hash."""
        assert hash_password("ab", "c") == hash_password("a", "bc")


# ---------------------------------------------------------------------------
# verify_token
# ---------------------------------------------------------------------------
class TestVerifyToken:
    def test_missing_token_none(self):
        with pytest.raises(HTTPException) as exc:
            verify_token(None)
        assert exc.value.status_code == 401
        assert exc.value.detail == "Missing token."

    def test_missing_token_empty_string(self):
        with pytest.raises(HTTPException) as exc:
            verify_token("")
        assert exc.value.status_code == 401
        assert exc.value.detail == "Missing token."

    @patch("utils.security.UserDao")
    def test_missing_token_does_not_query_db(self, mock_dao_cls):
        with pytest.raises(HTTPException):
            verify_token(None)
        mock_dao_cls.assert_not_called()

    @patch("utils.security.UserDao")
    def test_invalid_token(self, mock_dao_cls):
        mock_dao_cls.return_value.find_by_token.return_value = None

        with pytest.raises(HTTPException) as exc:
            verify_token("bad-token")

        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid token."
        mock_dao_cls.return_value.find_by_token.assert_called_once_with("bad-token")

    @patch("utils.security.UserDao")
    def test_valid_token_returns_user(self, mock_dao_cls):
        fake_user = MagicMock(name="user")
        mock_dao_cls.return_value.find_by_token.return_value = fake_user

        result = verify_token("good-token")

        assert result is fake_user
        mock_dao_cls.return_value.find_by_token.assert_called_once_with("good-token")


# ---------------------------------------------------------------------------
# generate_secret_HMAC_key
# ---------------------------------------------------------------------------
class TestGenerateSecretHMACKey:
    def test_returns_32_bytes(self):
        key = generate_secret_HMAC_key()
        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_keys_are_unique(self):
        keys = {generate_secret_HMAC_key() for _ in range(50)}
        assert len(keys) == 50

    @patch("utils.security.secrets.token_bytes", return_value=b"\x01" * 32)
    def test_uses_secrets_token_bytes(self, mock_tb):
        assert generate_secret_HMAC_key() == b"\x01" * 32
        mock_tb.assert_called_once_with(32)


# ---------------------------------------------------------------------------
# encode_secret_key
# ---------------------------------------------------------------------------
class TestEncodeSecretKey:
    def test_bytes_are_base64_encoded(self):
        key = b"\x00\x01\x02\xff"
        result = encode_secret_key(key)
        assert result == base64.b64encode(key).decode("ascii")
        assert isinstance(result, str)

    def test_str_is_returned_unchanged(self):
        assert encode_secret_key("already-a-string") == "already-a-string"

    def test_empty_bytes(self):
        assert encode_secret_key(b"") == ""

    def test_roundtrip(self):
        key = generate_secret_HMAC_key()
        assert base64.b64decode(encode_secret_key(key)) == key

    def test_generated_key_encoded_length(self):
        # 32 octets -> 44 caractères en base64 (avec padding)
        assert len(encode_secret_key(generate_secret_HMAC_key())) == 44


# ---------------------------------------------------------------------------
# generate_signature
# ---------------------------------------------------------------------------
class TestGenerateSignature:
    SECRET = b"s" * 32
    PROJECT = b"project-1"
    CODE = b"print('hello')"
    DEP = b"requests==2.31.0"

    def test_returns_32_bytes(self):
        sig = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        assert isinstance(sig, bytes)
        assert len(sig) == 32  # SHA-256

    def test_matches_manual_computation(self):
        h = hmac.new(self.SECRET, digestmod=hashlib.sha256)
        for part in (self.PROJECT, self.CODE, self.DEP):
            h.update(len(part).to_bytes(8, "big"))
            h.update(part)

        sig = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        assert sig == h.digest()

    def test_is_deterministic(self):
        a = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        b = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        assert a == b

    def test_different_secret_changes_signature(self):
        a = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        b = generate_signature(b"t" * 32, self.PROJECT, self.CODE, self.DEP)
        assert a != b

    @pytest.mark.parametrize(
        "project, code, dep",
        [
            (b"other", b"print('hello')", b"requests==2.31.0"),
            (b"project-1", b"print('bye')", b"requests==2.31.0"),
            (b"project-1", b"print('hello')", b"flask==3.0.0"),
        ],
    )
    def test_any_input_change_changes_signature(self, project, code, dep):
        original = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        assert generate_signature(self.SECRET, project, code, dep) != original

    def test_length_prefix_prevents_boundary_ambiguity(self):
        """Grâce au préfixe de longueur, déplacer des octets d'un champ à
        l'autre doit produire une signature différente."""
        a = generate_signature(self.SECRET, b"ab", b"c", b"d")
        b = generate_signature(self.SECRET, b"a", b"bc", b"d")
        c = generate_signature(self.SECRET, b"a", b"b", b"cd")
        assert len({a, b, c}) == 3

    def test_field_order_matters(self):
        a = generate_signature(self.SECRET, b"x", b"y", b"z")
        b = generate_signature(self.SECRET, b"y", b"x", b"z")
        assert a != b

    def test_empty_inputs(self):
        sig = generate_signature(self.SECRET, b"", b"", b"")
        assert len(sig) == 32

    def test_empty_inputs_differ_from_each_other_by_position(self):
        a = generate_signature(self.SECRET, b"x", b"", b"")
        b = generate_signature(self.SECRET, b"", b"x", b"")
        c = generate_signature(self.SECRET, b"", b"", b"x")
        assert len({a, b, c}) == 3

    def test_large_inputs(self):
        big = b"a" * 1_000_000
        sig = generate_signature(self.SECRET, self.PROJECT, big, big)
        assert len(sig) == 32

    def test_signature_can_be_verified_with_compare_digest(self):
        sig = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        again = generate_signature(self.SECRET, self.PROJECT, self.CODE, self.DEP)
        assert hmac.compare_digest(sig, again)
