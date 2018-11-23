import asyncio
from .Protocol import Protocol
from .ClientExceptions import *


class CLIENT(Protocol):
    def __init__(self, ip, port, *, client_encryption=None, loop=None):
        super().__init__(loop=loop, client_encryption=client_encryption)
        self.ip=ip
        self.port=port

        self.error_codes={'404':NotFound404Error, '403':ForbiddenRequestError}

    @asyncio.coroutine
    def connect(self) -> None:
        self.reader, self.writer = yield from asyncio.open_connection(self.ip, self.port,
                                                                      loop=self.loop)
        yield from self._start()
    
    @asyncio.coroutine
    def request(self, method:str, time_out=30, **kwargs) -> None or dict:
        """
        sends to server server a request and calling the decorator "on_recv" if the data recved
        if client has forbidden access to the request a ForbiddenRequestError will be raised
        if the server dosent have such a request a NotFound404Error will be raised
        if the server wont replay in the given time out a TimeoutError will be raised

        this method is safe to overwrite Becuse the only on who calls it the the module user
        """
        yield from self.send(method.upper(), **kwargs)
        try:
            method, data = yield from asyncio.wait_for(self.expected(method.upper(), *self.error_codes),
                                                       time_out, loop=self.loop
                                                      )
        except ValueError as e: # value error raised when the request recv unexpected method
            yield from self._call_decorated_function('on_error', error=e)
        else:
            if method in self.error_codes:
                raise self.error_codes[method]
            else:
                yield from self._call_decorated_function('on_recv', method=method, data=data)
    
    @asyncio.coroutine
    def handshake(self):
        method, data = yield from self.expected('HANDSHAKE', dencrypt=False)
        self.server_encryption.load_public_key(bytes(data['key'], encoding='utf-8'))

        yield from self.send('HANDSHAKE', key=str(self.client_encryption.public_key, encoding='utf-8'), encrypt=False)
        method, data = yield from self.expected('HANDSHAKE')
        self.id = data['id']

        yield from self.send('HANDSHAKE')

    @asyncio.coroutine
    def _start(self):
        try:
            yield from asyncio.wait_for(self.handshake(), 25,
                                        loop=self.loop)
        except Exception as e:
            yield from self._call_decorated_function('on_error', error=e)
        else:
            yield from self._run()
    
    @asyncio.coroutine
    def _run(self):
        asyncio.ensure_future(self.listen(), loop=self.loop)
        yield from self._call_decorated_function('on_connection')
    
    @asyncio.coroutine
    def listen(self):
        try:
            while True:
                try:
                    method, data = yield from self.recv()
                except Exception as e:
                    yield from self._call_decorated_function('on_error', error=e)
                else:
                    if method in self.error_codes:
                        raise self.error_codes[method]
                    yield from self._call_decorated_function('on_recv', method=method, data=data)
        except (ForbiddenRequestError, NotFound404Error): pass # the event listener dosent need to break because of those exceptions

    @asyncio.coroutine
    def _call_decorated_function(self, function_name, *args, **kwargs):
        try:
            yield from  getattr(self, function_name)(*args, **kwargs)
        except TypeError as e: pass # passing in case you didn't add the called decorator

    @classmethod
    def on_connection(cls, func):
        """docorator: called when client connected to the server"""
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_connection', func)
        return func
    
    @classmethod
    def on_recv(cls, func):
        """
        decorator: called when data recved from server
        args:
            client = your client
            method = the method the server sended
            data   = the data as a dict
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_recv', func)
        return func 

    @classmethod
    def on_error(cls, func):
        """
        decorator: called when client raising an error
        args:
            client = your client
            error  = the raised error
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_error', func)
        return func 

    @classmethod
    def on_server_error(cls, func):
        """
        decorator: if you send a requst some times the server send back a codes
        like 404="not found" or 403="assess not allowed"
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_server_error', func)
        return func
    
