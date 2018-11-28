import asyncio
from easyTCP.CLIENT.backend import CLIENT, ClientExceptions
from easyTCP.CLIENT.utils.functions import executer, args_to_dict

@CLIENT.on_connection
async def x(client):
    print("[+] Client connected to the SERVER (ip: %s, port: %d)" %(client.ip, client.port))

@CLIENT.on_recv
async def y(client, method, data):
    print('method: %s' %method)
    print(data)

@CLIENT.on_error
async def z(client, error):
    print('[!] EXCEPTION: %s' %error)


async def main(loop):
    client = CLIENT('127.0.0.1', 25569, loop=loop)
    
    await client.connect()
    while True:
        try:
            await executer(client, None, loop=loop)
        except ClientExceptions.NotFound404Error:
            print('server return 404 error')


if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.close()

