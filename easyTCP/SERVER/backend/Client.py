import asyncio, random
from .Protocol import Protocol


class CLIENT(Protocol):
    def __init__(self, reader, writer, server):
        super().__init__(reader, writer, loop=server.loop, server_encryption=server.encryption)
        self.server       = server
        self.is_superuser = False
        self.addr         = self.writer.get_extra_info('peername')
        self.password     = self.server.superuser_password
        self._id          = 0

    @property
    def id(self): # generating for the client a valid ID
        if self._id != 0 :
            return self._id
        _id = random.randint(6000, 9999)
        while _id in self.server._clients.keys():
            _id = random.randint(6000, 9999)
        self._id = _id
        return self._id

    @asyncio.coroutine
    def handshake(self):
        """
        handshake between the client and the server
        you can overwrite that handshake but the client needs to support the same handshake
        """ 
        yield from self.send('HANDSHAKE', key=str(self.server_encryption.public_key, encoding='utf-8'), encrypt=False) # need to send the first private key so all the recv packets will be encrypted

        method, data = yield from self.expected('HANDSHAKE', dencrypt=False)
        self.client_encryption.load_public_key(bytes(data['key'], encoding='utf-8'))
        # the clients suppost to send his public key for encryption
        # the recved packed suppost to be encrypted with the given public key

        yield from self.send('HANDSHAKE', id=self.id)
        # giving the client and ID that generated by the server

        method, data = yield from self.expected('HANDSHAKE')
        # confiming that the client recved the last package

        if data['type'].upper() == 'SUPERUSER': # client sends its type if its type is superuser we start in superuser handshake
            if self.password == data['password']: # better save password encrypted  (overwrite the handshake to do that)
                self.is_superuser = True
                yield from self.send('HANDSHAKE') # return handshake if the client menaged to login
            else:
                yield from self.send('401', reason='passwords dosent match login as norma client')

        yield from self.server.add_client(id=self.id, client=self)

    @asyncio.coroutine
    def start(self):
        """
        starting the CLIENT and waiting for handshake for 25 seconds if there is not handshake client will raise an ERROR
        so its better to use the decorator "on_client_error"
        """
        try:
            yield from asyncio.wait_for(self.handshake(),
                                        25, loop=self.loop)
        except Exception as e:
            yield from self.server._call_decorated_function('on_client_error', client=self, error=e)
        else:
            yield from self._run()

    @asyncio.coroutine
    def _run(self): # all the things to do when running for now it's only _listen
        yield from self._listen() 

    @asyncio.coroutine
    def _listen(self):
        """
        listening to the client for request or if he left
        """
        while True:
            try:
                method, data = yield from self.recv()
            except (ValueError ,ConnectionResetError): # happends when client close the connection
                yield from self.close_connection()
                break
            except Exception as e:
                yield from self.server._call_decorated_function('on_client_error', client=self, error=e)
            else:
                self.loop.create_task(self._prosses(method, data))
    
    @asyncio.coroutine
    def _prosses(self, method, data):
        """
        when the server recved data from the client by the _listen function
        the _prosses request see if the request is valid 
        
        most of those functions are not ment to bet overwrtied but if you want to you can
        """
        try:
            func = getattr(self.server, method.upper())
            # the decorator @add_request adding request automaticly and this called
            # the added requests (added request added via UPPERCASE name)

        except AttributeError as e:
            yield from self.server._call_decorated_function('on_client_unknown_request', client=self, request=method)
        else:
            try:
                _ = yield from func(client=self, **data)
                # the client arguments passed here
            except TypeError as e:
                yield from self.server._call_decorated_function('on_client_wrong_parameter', 
                            client=self, request=method, parameters=data
                        )
        
    @asyncio.coroutine
    def close_connection(self):
        """
        closing the connection between the server and the client and removing him from server clients
        raising: on_client_remove decorator
        """
        self.writer.close()
        yield from self.server.remove_client(id=self.id, client=self)

