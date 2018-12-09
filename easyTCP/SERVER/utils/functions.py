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

def external_modules(modules:list):
    """
    except Importing your external files for the @add_request
    all you need to do is put your extenal file name as you would import it
    example:
        external_modules(['<file_name>', ['<folder>.<file>']])
                                         - load the file from a folder
    """
    for module in modules:
        try:
            exec("import %s" %module)
        except ImportError:
            raise ModuleNotFoundError("Could not load %s" %module)

        
