import telepot

from ...registry import get_func_data, Trigger


class InlineTrigger(Trigger):
    def __init__(self):
        pass

    def test(self, update):
        return True

    def fire(self, update):
        return update.flavor == 'inline_query'

def on_inline_query(func):
    data = get_func_data(func)
    if data.trigger is None: data.trigger = InlineTrigger()
    elif not isinstance(data.trigger, InlineTrigger):
        raise Exception('Cannot attach an inline query trigger to a function with a trigger already specified!')
    return func
