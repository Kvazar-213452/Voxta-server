import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder
from nacl.exceptions import CryptoError

key = None

class EncryptedPacket:
    def __init__(self, ephemeral_pub_key: str, nonce: str, ciphertext: str):
        self.ephemeral_pub_key = ephemeral_pub_key
        self.nonce = nonce
        self.ciphertext = ciphertext

def generate_key_pair():
    key_pair = PrivateKey.generate()
    return {
        'publicKey': key_pair.public_key.encode(encoder=Base64Encoder).decode(),
        'privateKey': key_pair.encode(encoder=Base64Encoder).decode()
    }

def fast_encrypt(message: str, recipient_pub_key_b64: str):
    recipient_pub_key = PublicKey(recipient_pub_key_b64, encoder=Base64Encoder)
    ephemeral_key = PrivateKey.generate()
    box = Box(ephemeral_key, recipient_pub_key)

    nonce = nacl.utils.random(Box.NONCE_SIZE)
    ciphertext = box.encrypt(message.encode(), nonce)

    packet = EncryptedPacket(
        ephemeral_pub_key=ephemeral_key.public_key.encode(encoder=Base64Encoder).decode(),
        nonce=Base64Encoder.encode(nonce).decode(),
        ciphertext=Base64Encoder.encode(ciphertext.ciphertext).decode()
    )

    return {
        'packet': packet,
        'ephemeralPrivKey': ephemeral_key.encode(encoder=Base64Encoder).decode()
    }

def fast_decrypt(packet: dict, recipient_priv_key_b64: str) -> str:
    recipient_priv_key = PrivateKey(recipient_priv_key_b64, encoder=Base64Encoder)
    ephemeral_pub_key = PublicKey(packet["ephemeralPubKey"], encoder=Base64Encoder)
    box = Box(recipient_priv_key, ephemeral_pub_key)

    nonce = Base64Encoder.decode(packet["nonce"])
    ciphertext = Base64Encoder.decode(packet["ciphertext"])

    try:
        decrypted = box.decrypt(ciphertext, nonce)
    except CryptoError:
        raise Exception("Decryption failed")

    return decrypted.decode()

# ========= key =========
def init_key_lite():
    global key
    key = generate_key_pair()

def get_key_lite():
    return key
