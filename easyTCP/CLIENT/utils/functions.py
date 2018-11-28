import asyncio
from ..backend import CLIENT


async def args_to_dict(*args):
    """
    convert string to dict to send data to the server
    x = 'echo -m this the value'
    converted_to_list = x.split('-')

    await args_to_dict(*converted_to_list)
    

    will return 
        echo, {'m':'this the value'}

    better write your own version
    """
    method = args[0]
    values = {}

    for i in args[1:]:
        _ = i.split()
        values[_[0]]=i[len(_[0]) +1:]
    return method.strip(), values

async def executer(client, time_out=10, *,loop=asyncio.get_event_loop()):
    """
    this is for fast testing you can use it for your projects or somthing but this is very basic and poor
    DO NOT use executer like this is mostliy for fast testing sure you have more ideas for how to make a nice looking code and more dynamic
    """
    while True:
        x = await loop.run_in_executor(None, input, '>>> ')
        if len(x.strip()) == 0:
            continue

        args = x.split('-')
        try:
            method, values = await args_to_dict(*args) # conert the string to dict
            # >>> echo -m a text
            # will return liket this | 'echo', {'m': 'a text'} |

        except IndexError:
            print('Missing Indexs')
        else:
            asyncio.ensure_future(client.request(time_out=time_out,
                                    method=method, **values), loop=loop)

