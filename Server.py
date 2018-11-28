import asyncio
from easyTCP.SERVER.backend import SERVER
from easyTCP.SERVER.utils import DEFAULT_SETTINGS, DEFAULT_ENCRYPTION
from easyTCP.SERVER.utils.decorators import add_request
from easyTCP.SERVER.utils.BUILD_IN import BUILD_IN # importing base requests like help or echo


@SERVER.on_ready
async def server_is_ready(server):
    print('[+] Server started running (ip: %s, port: %d)' %(server.ip, server.port))

@SERVER.on_error
async def got_error(server, error):
    print('[!] SERVER ERROR:')
    raise error

@SERVER.on_client_join
async def joined(server, client, id):
    print('[+] A new client joined with the ID: %d' %id)
    await client.send('HELLO', message='this is a banner when client joined')

@SERVER.on_client_remove
async def removed(server, id):
    print('[-] [%d] left the server' %id)

@SERVER.on_client_unknown_request
async def unknown_request(server, client, request):
    print('[?] unknown request sended from %d [%s]' %(client.id, request))
    # you can send 404 error and that will raise error on the other side
    await client.send('404')

@SERVER.on_client_wrong_parameter
async def wrong_parameters(server, client, request, parameters):
    print('[+] client entered wrong parameters for [%s] %s' %(request, parameters))
    # you can send the client how to use the request or some code error

@SERVER.on_client_error
async def client_error(server, client, error):
    print('[!] client [%d] raised %s' %(client.id, error))


@add_request # example
async def test(server, client, h, d='default'):
    print('h = %s\nd = %s' %(h, d))


async def main(loop):
    server = SERVER('127.0.0.1', 25569, None, settings=DEFAULT_SETTINGS, loop=loop)
    await server.start()


if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.close()


