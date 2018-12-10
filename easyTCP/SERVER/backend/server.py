import asyncio
from .Client import CLIENT


class SERVER:
    client = CLIENT

    client_functions     = [] # make this easier to see stuff 
    superuser_functions  = []

    def __init__(self, IP:str, PORT:int, encryption, 
                    *, settings, superuser_password, loop=None):
        self.ip   = IP
        self.port = PORT

        self.superuser_password = superuser_password
        self.settings       = settings
        self.encryption     = encryption
        self.loop           = loop or asyncio.get_event_loop()

        self._clients = {}
        self._superusers  = {}
    
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
        if client.is_superuser:
            self._superusers[id] = client
        else:
            self._clients[id] = client
        yield from self._call_decorated_function('on_client_join', id=id, client=client)

    @asyncio.coroutine
    def remove_client(self, id, client):
        """remove that client from server clients via given ID and calling decorator: on_client_remove"""
        try:
            if client.is_superuser:
                del self._superusers[id]
            else:
                del self._clients[id]
        except KeyError: pass
        finally:
            yield from self._call_decorated_function('on_client_remove', id=id)
    
    @asyncio.coroutine
    def close(self, error=None):
        """closing existing connections and the server"""
        self.server.close()
        for _, client in self._clients.items():
            self.loop.create_task(client.writer.close())
            # if it take time for some reason or if you have a lot of clients
            # they wont be have to wait for one connection to close
            # in the *.close() leaves existing connections open

        for _, client in self._superusers.items():
            self.loop.create_task(client.writer.close())
            # doing the same for the superusers

        self._clients={}
        self._superusers={}
        yield from self._call_decorated_function('on_close', error=error)
    
    @asyncio.coroutine
    def keep_alive(self):
        """function must be called if you starting the server as a context managment
        (the "with" statement)"""
        while self.loop.is_running:
            yield from asyncio.sleep(10)

    @asyncio.coroutine
    def _call_decorated_function(self, function_name, *args, **kwargs):
        try:
            yield from getattr(self, function_name)(**kwargs)
        except TypeError: pass

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
    def on_close(cls, func):
        """
        decorator: called after server closed becuase of error or the function "close" or if you doing loop.close()
        args passing:
            first_arg = server

            error = if the server closed because of some error
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError('%s is not coroutine function' %(func.__name__))
        setattr(cls, 'on_close', func)
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
        return self.ip, self.port

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close(exc_val)

