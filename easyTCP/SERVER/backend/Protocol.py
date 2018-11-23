import asyncio
import json
from utils import DEFAULT_SETTINGS
from utils.DEFAULT_ENCRYPTION import SERVER_encryption, CLIENT_encryption


def json_dumper(data):
    """converts the data to a valid json string and return bytes"""
    data = json.dumps(data)
    return bytes(data, encoding=DEFAULT_SETTINGS.ENCODING)

def json_loader(data):
    """converts the data to a string and return a python dict"""
    return json.loads(str(data, encoding=DEFAULT_SETTINGS.ENCODING))


class Protocol(object):
    def __init__(self, reader, writer, *, loop=None, server_encryption=None):
        self.reader=reader
        self.writer=writer

        self.loop=loop or asyncio.get_event_loop()
        self.server_encryption = server_encryption or SERVER_encryption(encoding=DEFAULT_SETTINGS.ENCODING)
        self.client_encryption = CLIENT_encryption(DEFAULT_SETTINGS.ENCODING)

        self.jload = json_loader
        self.jdump = json_dumper

    @asyncio.coroutine
    def send(self, method, *, drain=False, encrypt=True, **kwargs):
        """
        CORE:
            sends the data first prameter is the method
            all the rest must be key arguments

            not_valid_key_arguments:
                drain, encrypted
            
            those argument for people who know when to use them

            drain = self.wrtier.drain()
            encrypted = if to encrypt the data
            """
        data = self.jdump({'method':method, **kwargs})
        if encrypt: # we don't need to encrypt the data when we want to send the public key 
            data = self.client_encryption.encrypt(data) # the client wont be able to read the encrypted packet
        self.writer.write(data)

        if drain:
            yield from self.writer.drain()

    @asyncio.coroutine
    def recv(self, dencrypt=True):
        """
        CORE:
            waiting for data and when recved return method, data

            prameters:
                dencrypt = if your client sends you the data not encrypted you dont need to dencrypted it or if you just want the enctypted data ._. 
        """
        data = yield from self.reader.read(DEFAULT_SETTINGS.READ_SIZE)
        if dencrypt:
            data = self.server_encryption.dencrypt(data) # the recved data suppost to be encrypted via server public key
        data = self.jload(data)

        return data['method'], {k:i for k, i in data.items() if k != 'method'}

    @asyncio.coroutine
    def expected(self, *args, dencrypt=True):
        """
        gose to the recv function and check if the method is in one of the expeted given arguments
        if not it will raise ValueError

        for example

        you send echo request and you expect echo back or some 404 error somthing like that
        but the server return test
        that will raise ValueError
        """
        method, _ = yield from self.recv(dencrypt)
        if args and method not in method:
            raise ValueError('expected %s recved %s' %(args, method))
        return method, _
        
