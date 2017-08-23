from ...registry import get_func_data


def private(func):
    data = get_func_data(func)
    data.chat_type.append('private')
    return func

def group(func):
    data = get_func_data(func)
    data.chat_type.append('group')
    return func

def supergroup(func):
    data = get_func_data(func)
    data.chat_type.append('supergroup')
    return func
