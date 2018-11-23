import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes


class ENCRYPTION_BASE(object):

    def encrypt(self, text):
        """send to the client to encrypt messages"""
        encrypted = self.public_key.encrypt(
            bytes(text, encoding=self.encoding) if type(text) != bytes else text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return base64.b64encode(encrypted)

    def dencrypt(self, text):
        """DO NOT SEND THIS KEY used to decrypt messages"""
        text = base64.b64decode(text)

        decrypted = self.private_key.decrypt(
            text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return decrypted

    def save_private_key(self, file='key'):
        key = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        try:
            with open(file, 'x')as f:
                pass
        except FileExistsError: pass
        finally:
            with open(file, 'wb')as f:
                f.write(key)
    
    def load_private_key(self, key):
        from cryptography.hazmat.primitives.serialization import load_pem_private_key

        self.private_key=load_pem_private_key(key, None, default_backend())
        self.public_key = self.private_key.public_key()
        self.key = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
    
    def load_public_key(self, key):
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        self.public_key=load_pem_public_key(key, default_backend())


class CLIENT_encryption(ENCRYPTION_BASE):
    def __init__(self, encoding='utf-8'):
        self.private_key = rsa.generate_private_key(
            public_exponent=32769,
            key_size=4096,
            backend=default_backend()
        )

        self._public_key = self.private_key.public_key()
        self.public_key = self._public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
        self.encoding=encoding
    
    def load_public_key(self, key):
        raise NotImplementedError


class SERVER_encryption(ENCRYPTION_BASE):
    def __init__(self, encoding='utf-8'):
        self.public_key=None
        self.encoding=encoding
    
    def load_private_key(self, key):
        raise NotImplementedError
    
    def save_private_key(self, file='key'):
        raise NotImplementedError

    def dencrypt(self, text):
        raise NotImplementedError

        