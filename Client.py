import asyncio
from easyTCP.CLIENT.backend import CLIENT, ClientExceptions
from easyTCP.CLIENT.utils.functions import executer, args_to_dict

@CLIENT.on_connection
async def x(client):
    print("[+] Client connected to the SERVER (ip: %s, port: %d)" %(client.ip, client.port))

@CLIENT.on_disconnect
async def u(client):
    print("disconnected from server")

@CLIENT.on_recv
async def y(client, method, data):
    if method == 'HELP':
        print('help:')
        print(data['doc']) # did this to make it readable
    else:
        print(method, '\n', data)

@CLIENT.on_error
async def z(client, error):
    raise error


async def main(loop):
    client = CLIENT('127.0.0.1', 25569, admin_password='123', loop=loop)
    
    await client.connect()
    await executer(client, None, loop=loop)

    await client.close()


if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.close()

