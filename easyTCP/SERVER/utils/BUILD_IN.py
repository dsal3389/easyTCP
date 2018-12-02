import asyncio
from .decorators import add_request, admin_required


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
    async def commands(server, client):
        """show all the commands that the client can user
        include the admin commands"""
        commands = [command.title() for command in dir(server) if not command.startswith('_') and command.upper() == command]
        await client.send('COMMANDS', commands=commands)

    @add_request
    @admin_required
    async def bc(server, client, m, t='client'):
        """send broadcast to all clients (only for admins)
            -m <message>        the message to broadcast
            -t <client/admin>   to who send the message as default its "client"
            
            example:
                >>> bc -t admin -m message only for admins
            
            Bcuz I did "-t admin" only admins will recv that message
        """
        if t.lower() == 'client':
            await asyncio.wait([client.send('BC', id=str(client.id), message=m) for id, client in server._clients.items()])
            await asyncio.wait([client.send('BC', id=str(client.id), message=m) for id, client in server._admins.items()])
            # admins can recv bc for clients

        elif t.lower() == 'admin':
            await asyncio.wait([client.send('BC', id=str(client.id), message=m) for id, client in server._admins.items()])
        else:
            await client.send('406', reason='unknown %s' %t)
    
    @add_request
    @admin_required
    async def clients(server, client, e=None):
        """give you the list of clients ids to see who connected (only for admins)
            -e (exclude[client/admin])  for example if you exclude admin this wont show the admins that connected

            example:
                >>> clients -e admin
                # will return only the clients ids
            dont call 'e' to show admins and clients    
        """
        if e is None:
            clients = {
                'admins' :[client_id for client_id in server._admins],
                'clients':[client_id for client_id in server._clients]
            }
        elif e.lower() == 'admin':
            clients = {'clients':[client_id for client_id in server._clients]}
        elif e.lower() == 'client':
            clients = {'admins':[client_id for client_id in server._admins]}
        else:
            clients = {e:[]}

        await client.send('CLIENTS', **clients)


if __name__!='__main__':
    print('[+] BUILD_IN functions loaded')
