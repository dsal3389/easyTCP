import asyncio
from .decorators import add_request, superuser


class BUILD_IN:

    @add_request
    async def echo(server, client, m, *args, **kwargs):
        """display message to the server terminal
            -m <message>    display the message to the screen
        """
        print('[+]Client [%d] echo:' %client.id, m)
    
    @add_request
    async def ping(server, client, **kwargs):
        await client.send('HELLO')

    @add_request
    async def help(server, client, f, *args, **kwargs):
        """shows help for other requests
            -f <command>    return help for the given command
        """
        try:
            func = getattr(server, f.upper())
        except AttributeError:
            await client.send('404', reason='request %s not found' %f)
        else:
            doc = func.__doc__
            await client.send('HELP', doc=doc)
    
    @add_request
    async def commands(server, client, a='none'):
        """show all the commands that the client can user
        include the superuser commands"""
        commands = {'client': server.client_functions}
        if client.is_superuser and a != 'none':
            commands['superuser'] = server.superuser_functions

        await client.send('COMMANDS', **commands)

    @superuser
    @add_request
    async def bc(server, client, m, t='client'):
        """send broadcast to all clients (only for superusers)
            -m <message>        the message to broadcast
            -t <client/superuser>   to who send the message as default its "client"
            
            example:
                >>> bc -t superuser -m message only for superusers
            
            Bcuz I did "-t superuser" only superusers will recv that message
        """
        if t.lower() == 'client':
            await asyncio.wait([client.send('BC', id=str(client.id), message=m) for id, client in server._clients.items()])
            await asyncio.wait([client.send('BC', id=str(client.id), message=m) for id, client in server._superusers.items()])
            # superusers can recv bc for clients

        elif t.lower() == 'superuser':
            await asyncio.wait([client.send('BC', id=str(client.id), message=m) for id, client in server._superusers.items()])
        else:
            await client.send('406', reason='unknown %s' %t)

    @superuser
    @add_request
    async def clients(server, client, e=None):
        """give you the list of clients ids to see who connected (only for superusers)
            -e (exclude[client/superuser])  for example if you exclude superuser this wont show the superusers that connected

            example:
                >>> clients -e superuser
                # will return only the clients ids
            dont call 'e' to show superusers and clients    
        """
        if e is None:
            clients = {
                'superusers' :[client_id for client_id in server._superusers],
                'clients':[client_id for client_id in server._clients]
            }
        elif e.lower() == 'superuser':
            clients = {'clients':[client_id for client_id in server._clients]}
        elif e.lower() == 'client':
            clients = {'superusers':[client_id for client_id in server._superusers]}
        else:
            clients = {e:[]}

        await client.send('CLIENTS', **clients)


if __name__!='__main__':
    print('[+] BUILD_IN functions loaded')
