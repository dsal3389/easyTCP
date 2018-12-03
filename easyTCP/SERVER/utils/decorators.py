import asyncio
from ..backend import SERVER
from functools import wraps


def add_request(func):
    """
    to add request that the clients can request easliy
    your functions parameters are the request arguments
    and you functions __doc__ is your help for the function

    > as prameters you will always get client and server
        first prameter is the server

    how to use:

    @add_request
    async def test(server, m, s='default', **kwargs):
        print('m =', m)
        print('s =', s)

    CLIENT:
        >>> test -m test passed

    SERVER:
        m = test passed
        s = default

    or 

    CLIENT:
        >>> test -m testing -s not default

    SERVER:
        m = testing
        s = not default

    if the client wont enter a required prameter the server will call 
    the decorator: on_client_wrong_parameter
    """
    name = func.__name__
    coroutine = asyncio.iscoroutinefunction(func)

    if not coroutine:
        raise ValueError('the request "%s" is not coroutine' %name)
    setattr(SERVER, name.upper(), func) # all added requests added in uppercase
    SERVER.client_functions.append(func.__name__.lower())

    return func

def superuser(func):
    """
    if the client that requested is not an superuser
    the server will return 403
    """
    del SERVER.client_functions[SERVER.client_functions.index(func.__name__)]
    # deletes the function from the client functions list

    SERVER.superuser_functions.append(func.__name__.lower())

    @wraps(func)
    async def wrapper(server, client, *args, **kwargs):
        if client.is_superuser:
            await func(server, client, *args, **kwargs)
        else: 
            await client.send('403')
    return wrapper
