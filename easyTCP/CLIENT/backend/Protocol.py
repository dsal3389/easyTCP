import asyncio
import json
from utils import DEFAULT_SETTINGS
from utils.DEFAULT_ENCRYPTION import SERVER_encryption, CLIENT_encryption


def json_dumper(data):
    return bytes(json.dumps(data), encoding=DEFAULT_SETTINGS.ENCODING)

def json_loader(data):
    return json.loads(str(data, encoding=DEFAULT_SETTINGS.ENCODING))


class Protocol(object):
    def __init__(self, reader=None, writer=None, *, loop=None, client_encryption=None):
        self.reader=reader
        self.writer=writer

        self.loop=loop or asyncio.get_event_loop()
        self.server_encryption = SERVER_encryption(DEFAULT_SETTINGS.ENCODING)
        self.client_encryption = client_encryption or CLIENT_encryption(encoding=DEFAULT_SETTINGS.ENCODING)

        self.jload = json_loader
        self.jdump = json_dumper

    @asyncio.coroutine
    def send(self, method, *, drain=False, encrypt=True, **kwargs):
        data = self.jdump({'method':method.upper(), **kwargs})
        if encrypt: # we don't need to encrypt the data when we want to send the public key 
            data = self.server_encryption.encrypt(data) # the client wont be able to read the encrypted packet
        self.writer.write(data)

        if drain:
            yield from self.writer.drain()

    @asyncio.coroutine
    def recv(self, dencrypt=True):
        data = yield from self.reader.read(DEFAULT_SETTINGS.READ_SIZE)
        if dencrypt:
            data = self.client_encryption.dencrypt(data)
        data = self.jload(data)

        return data['method'], {k:i for k, i in data.items() if k != 'method'}

    @asyncio.coroutine
    def expected(self, *args, dencrypt=True):
        method, _ = yield from self.recv(dencrypt)
        if args and method not in method:
            raise ValueError('expected %s recved %s' %(args, method))
        return method, _
        
