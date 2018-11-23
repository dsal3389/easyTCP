import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes


class ENCRYPTION_BASE(object):

    def encrypt(self, text):
        """
        called when ever server wants to send data to client 
        encrypte the data via client public_key

        overwrite:
            when overwriting this make sure you get 1 parameter and that the data the server want to send
            make sure the passed text is bytes and encrypte it
        """
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
        """
        called when ever the client send encrypted message with the given public key
        from the server

        overwrite:
            to overwrite pls make sure you get the text parameter
            thats a encrypted data and encrypt it with your own private key
            (the function name need to be the same "dencrypt")
        """
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
        """if you want to save you current private key accept generating new one every time"""
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
        """
        loading key
        if you saved a key via save_private_key
        do 

        with open(<your_file>, 'rb') as f:
            key = f.read()
        enc.load_private_key(key)

        and from now the saved key will be the main private key
        """
        from cryptography.hazmat.primitives.serialization import load_pem_private_key

        self.private_key=load_pem_private_key(key, None, default_backend())
        self.public_key = self.private_key.public_key()
        self.key = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
    
    def load_public_key(self, key):
        """
        loading the given public key for encryption
        
        overwrite:
            when you overwrite this function pls make sure you get 1 parameter and thats the key
            (keep the same name "load_public_key")
        """
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        self.public_key=load_pem_public_key(key, default_backend())
    
    def __repr__(self):
        return 'to overwrite this module and make your own encryption pls call the function name as they are here'


class SERVER_encryption(ENCRYPTION_BASE):
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


class CLIENT_encryption(ENCRYPTION_BASE):
    def __init__(self, encoding='utf-8'):
        self.public_key=None
        self.encoding=encoding
    
    # rasing NotImplementedError Bcus client dont need those
    # functions so when using then you will get an error

    def load_private_key(self, key):
        raise NotImplementedError
    
    def save_private_key(self, file='key'):
        raise NotImplementedError

    def dencrypt(self, text):
        raise NotImplementedError

        