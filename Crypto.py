import ecdsa
from hashlib import sha256


def validate_signature(verification_key: str, message: str, signature: str):
    message = bytes(message, encoding="ascii")
    signature = bytes.fromhex(signature)
    verification_key = bytes.fromhex(verification_key)
    vk = ecdsa.VerifyingKey.from_string(verification_key, curve=ecdsa.SECP256k1, hashfunc=sha256)
    try:
        return vk.verify(signature, message, hashfunc=sha256)
    except ecdsa.BadSignatureError:
        return False


def generate_keys():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return str(sk.to_string().hex()), str(vk.to_string(encoding="raw").hex())


def sign(signing_key: str, message: str):
    signing_key = bytes.fromhex(signing_key)
    vk = ecdsa.SigningKey.from_string(signing_key, curve=ecdsa.SECP256k1, hashfunc=sha256)
    message = bytes(message, encoding="ascii")
    signature = vk.sign(message, hashfunc=sha256)
    return str(signature.hex())

