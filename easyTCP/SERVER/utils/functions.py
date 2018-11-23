

def load_external_files(*args):
    for file in args:
        try:
            eval('import %s' %file)
        except ImportError as e:
            raise ImportError('colud load %s make sure you the file is in your project dir ' 
                        %file) from e
