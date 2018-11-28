import asyncio
from .Client import CLIENT


class SERVER:
    client = CLIENT

    def __init__(self, IP, PORT, encryption, *, settings, loop=None):
        self.ip = IP
        self.port = PORT

        self.settings = settings
        self.encryption = encryption
        self.loop=loop or asyncio.get_event_loop()

        self._clients = {}
    
    @asyncio.coroutine
    def start(self):
        """start the server on your given port and IP"""
        self.server = yield from asyncio.start_server(self.handle_connection,
                                                      self.ip, self.port)
        yield from self._call_decorated_function('on_ready')

    @asyncio.coroutine
    def handle_connection(self, reader, writer):
        client = self.client(reader, writer, self)
        asyncio.ensure_future(client.start(), loop=self.loop)

    @asyncio.coroutine
    def add_client(self, id, client):
        """adding client object to client list in the server calling decorator: on_client_join"""
        self._clients[id] = client
        yield from self._call_decorated_function('on_client_join', id=id, client=client)
    
    @asyncio.coroutine
    def remove_client(self, id):
        """remove that client from server clients via given ID and calling decorator: on_client_remove"""
        try:
            del self._clients[id]
        except KeyError: pass
        finally:
            yield from self._call_decorated_function('on_client_remove', id=id)

    @asyncio.coroutine
    def _call_decorated_function(self, function_name, *args, **kwargs):
        try:
            yield from getattr(self, function_name)(**kwargs)
        except TypeError as e: pass

    @classmethod
    def on_ready(cls, func):
        """decorator: called after server started
        args passing:
            first_arg = server
            
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_ready', func)
        return func

    @classmethod
    def on_error(cls, func):
        """
        decorator: called after server raised error
        args passing:
            first_arg = server

        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_error', func)
        return func    

    @classmethod
    def on_client_join(cls, func):
        """
        decorator: called when client passed handshake and join
        args passing:
            first_arg = server

            client = the joined client
            id     = the client joined id
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_client_join', func)
        return func

    @classmethod
    def on_client_remove(cls, func):
        """
        decorator: called when client left or removed by error
        args passing:
            first_arg = server

            id = the removed client id
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_client_remove', func)
        return func
    
    @classmethod
    def on_client_error(cls, func):
        """
        called when client raise error
        args passing:
            first_arg = server

            client = the client that raised the error
            error  = the error itself
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_client_error', func)
        return func
    
    @classmethod
    def on_client_unknown_request(cls, func):
        """
        decorator: called when unknown request recved
        args passing:
            first_arg = server

            client  = the client that sended the request
            request = what the client sended 
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_client_unknown_request', func)
        return func
    
    @classmethod
    def on_client_wrong_parameter(cls, func):
        """
        decorator: called when unknown request recved
        args passing:
            first_arg = server

            client  = the client that sended the request
            request = what the client sended 
            parameters = entered as a dict the client parameters
        
        note!: you can silent this if you add at the end of your request **kwargs
        if you still getting this decorator called after you muted it with **kwargs or the client enter the right paramters thats
        mean you have problem with your function
        
        request is the function that you add with the decorator @add_request
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_client_wrong_parameter', func)
        return func

    def __str__(self):
        return "SERVER"

