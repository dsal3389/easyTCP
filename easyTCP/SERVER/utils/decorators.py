import asyncio
from backend import SERVER


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
    setattr(SERVER, name.upper(), func)