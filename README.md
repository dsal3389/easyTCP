[![PyPI](https://img.shields.io/apm/l/vim-mode.svg?style=flat-square)](https://github.com/dsal3389/easyTCP/blob/master/LICENSE)
[![](https://img.shields.io/pypi/pyversions/Django.svg?style=flat-square)](https://pypi.org/project/easyTCP/#description)

# easyTCP
an esay way to user async server

# installing
`python3 -m pip3 install easyTCP`

### example
files for example [here][examples].

[examples]: https://github.com/dsal3389/easyTCP/tree/master/example

### what you get
- encryption
- BUILD IN requests
- user level `superuser/normal user`

### Quick start
```py
import asyncio
from easyTCP.SERVER.backend import SERVER
from easyTCP.SERVER.utils import DEFAULT_SETTINGS
from easyTCP.SERVER.utils.BUILD_IN import BUILD_IN


@SERVER.on_ready
async def x(server):
	print("[+] SERVER started (IP: %s | PORT: %d)" %(server.ip, server.port))

async def main(loop):
    server = SERVER('127.0.0.1', 25569, None, settings=DEFAULT_SETTINGS, superuser_password='123', loop=loop)
    await server.start()

if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.close()
```
**this is a server that only show when he is ready but everything is still working like `removing/adding` clients
and build in commands are loaded**
