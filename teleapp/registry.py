registers = {}


def get_registered():
    return registers

def get_func_data(func):
    global registers
    if func not in registers:
        registers[func] = FuncData(func)
    return registers[func]

class Trigger:
    def __init__(self):
        pass

    def test(self, update):
        ''' Checks if the trigger has any hope of firing. '''
        return False

    def fire(self, update):
        ''' Should return true of the attempt was successful. Return True or a
        tuple of (args, kwargs) to fire the function. False will continue
        checking triggers until one successfully fires. '''
        return False

class FuncData:
    def __init__(self, func):
        self.func = func

        self.content_type = []
        self.chat_type = []
        self.chat_id = []

        self.trigger = None

    def test(self, update):
        if len(self.content_type) != 0 and update.content_type not in self.content_type:
            return False
        if len(self.chat_type) != 0 and update.chat_type not in self.chat_type:
            return False
        if len(self.chat_id) != 0 and update.chat_id not in self.chat_id:
            return False
        return self.trigger.test(update)

    def fire(self, update):
        ret = self.trigger.fire(update)
        if ret is True:
            self.func(update)
            return True
        if type(ret) is tuple or type(ret) is list:
            if len(ret) == 1:
                self.func(update, *ret[0])
            elif len(ret) == 2:
                self.func(update, *ret[0], **ret[1])
            return True
        return False
