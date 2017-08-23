import re

from ...registry import get_func_data, Trigger


class TextTrigger(Trigger):
    def __init__(self):
        self.captures = []

    def test(self, update):
        if 'edit_date' in update.raw: return False
        return update.text is not None

    def fire(self, update):
        for capture in self.captures:
            ret = capture(update.text)
            if ret:
                if type(ret) is list or type(ret) is tuple:
                    return (ret,)
                return True
        return False

def regex_parse(regex, test, sensitive):
    match = re.search(regex, test) if sensitive else re.search(regex, test, flags=re.IGNORECASE)
    if not match: return False
    groups = match.groups()
    if len(groups) == 0:
        return True
    return groups

def regex(regex, sensitive=False):
    def inner(func):
        data = get_func_data(func)
        if data.trigger is None: data.trigger = TextTrigger()
        elif not isinstance(data.trigger, TextTrigger):
            raise Exception('Cannot attach a text trigger to a function with a trigger already specified!')

        data.trigger.captures.append(lambda text: regex_parse(regex, text, sensitive=sensitive))

        return func
    return inner

def contains(text, sensitive=False):
    return regex(text, sensitive=sensitive)

def equals(text, sensitive=False):
    return regex('^' + text + '$', sensitive=sensitive)
