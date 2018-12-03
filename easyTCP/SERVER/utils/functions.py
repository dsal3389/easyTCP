from ..backend import SERVER

def exclude(functions:list):
    """excluding functions from the server
    lets say you want to spacific function from the BUILD_IN
    just enter here all the functions you dont want ofc you need to load them first
    
    example:
        exclude(['echo', 'commands'])
        # deletes only those functions from the server
    """
    for func in functions:
        
        #check if the func in the server and dosents starts with '_'
        if func.upper() in dir(SERVER) and not func.startswith('_'):
            if func.lower() in SERVER.client_functions:
                del SERVER.client_functions[SERVER.client_functions.index(func.lower())] # delets if from the client function list
            elif func.lower() in SERVER.superuser_functions:
                del SERVER.superuser_functions[SERVER.superuser_functions.index(func.lower())] # same just for superusers

            exec('del SERVER.%s' %func.upper())


        
