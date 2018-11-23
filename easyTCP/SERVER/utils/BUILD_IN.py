import asyncio
from .decorators import add_request


class BUILD_IN:

    @add_request
    async def echo(server, client, m, *args, **kwargs):
        """display message to the server terminal"""
        print('[+]Client [%d] echo:' %client.id, m)
    
    @add_request
    async def ping(server, client, **kwargs):
        await client.send('PING', hello='hello')

    @add_request
    async def help(server, client, f, *args, **kwargs):
        """shows help for other requests"""
        try:
            func = getattr(server, f.upper())
        except AttributeError:
            await client.send('404', reason='request %s not found' %f)
        else:
            doc = func.__doc__
            await client.send('HELP', doc=doc)


if __name__!='__main__':
    print('BUILD_IN functions loaded')
