import asyncio
from easyTCP.SERVER.backend import SERVER
from easyTCP.SERVER.utils import DEFAULT_SETTINGS, DEFAULT_ENCRYPTION
from easyTCP.SERVER.utils.decorators import add_request, superuser
from easyTCP.SERVER.utils.BUILD_IN import BUILD_IN # importing base requests like help or echo
from easyTCP.SERVER.utils.functions import exclude, external_modules


@SERVER.on_ready
async def server_is_ready(server):
    print('[+] Server started running (ip: %s, port: %d)' %(server.ip, server.port))

@SERVER.on_close
async def closed(server, error):
    if error is not None:
        raise error
    print("[-] Server closed")

@SERVER.on_client_join
async def joined(server, client, id):
    if client.is_superuser:
        print('[+] an superuser joined [%d]' %client.id)
    else:
        print('[+] A new client joined with the ID: %d' %id)
    await client.send('HELLO', message='this is a banner when client joined')

@SERVER.on_client_remove
async def removed(server, id):
    print('[-] [%d] left the server' %id)

@SERVER.on_client_unknown_request
async def unknown_request(server, client, request):
    print('[?] unknown request sended from %d [%s]' %(client.id, request))
    await client.send('404')
    # this will raise exception on the client side

@SERVER.on_client_wrong_parameter
async def wrong_parameters(server, client, request, parameters):
    if client.is_superuser:
        print('[~] superuser entered wrong parameters for [%s] %s' %(request, parameters))
    else:
        print('[~] client entered wrong parameters for [%s] %s' %(request, parameters))
    await server.HELP(client=client, f=request)
    # sending the client the help of the requested function
    # note: every function added upper case thats why I did "HELP" and not "help"
    # ofc you need to provide the functions the right parameters in that case I have added client and f Bcuz that what we need

@SERVER.on_client_error
async def client_error(server, client, error):
    print('[!] client [%d] raised %s' %(client.id, error))

@superuser
@add_request # example
async def test(server, client, h, d='default'):
    print('h = %s\nd = %s' %(h, d))


async def main(loop):
    exclude(['test']) # deleting the example in line 54

    async with SERVER('127.0.0.1', 25569, None, settings=DEFAULT_SETTINGS, superuser_password='123', loop=loop) as server:
            await server.start()

            await asyncio.wait_for(
                server.keep_alive(), 20, loop=loop
            ) # running the server for 20 sec to show you the on_close decorator
              # importent note: if you opening the server with "with"
              # you must call the keep_alive function (do not run this as a task)
              # as normal you should call this like this:
              # await server.keep_alive()


if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
        # this is not importent anymore while the keep_alive function running
        # so if you want to stop the loop call loop.close() this will close the server as well
        # or you can call server.close() this wont stop the run_forever but the server only

    finally:
        loop.close()
