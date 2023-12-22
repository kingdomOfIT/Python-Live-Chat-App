from jinja2 import Undefined


def _slice(iterable, pattern):
    """
    A custom built slice method that can be used inside jinja template enginer
    """
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    
    #convert to list so we can slice
    items = str(iterable)
    
    start = None
    end = None
    stribe = None
    
    #split pattern into slice components
    if pattern: 
        tokens = pattern.split(':')
        print(tokens)
        if len(tokens) > 1:
            start = int(tokens[0])
        if len(tokens) > 2:
            end = int(tokens[1])
        if len(tokens) > 3:
            stribe = int(tokens[2])
    
    return items[start:end:stribe]