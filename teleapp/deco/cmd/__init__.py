from ...registry import get_func_data, Trigger

from .. import get_default_args


class CommandTrigger(Trigger):
    def __init__(self, command):
        self.command = command
        self.args = []
        self.kwargs = []

    def test(self, msg):
        return msg.text is not None and msg.text[:1] == '/'

    def fire(self, msg):
        cmd_split = None
        if msg.text.startswith('/%s@%s' % (self.command, msg.bot.username)):
            cmd_split = msg.text.split('/%s@%s ' % (self.command, msg.bot.username), 1)
        elif msg.text.startswith('/%s' % self.command):
            cmd_split = msg.text.split('/%s ' % self.command, 1)

        if cmd_split is None:
            return False

        min_args = len(self.args)
        max_args = len(self.args) + len(self.kwargs)

        args = []
        kwargs = []
        if len(cmd_split) > 1:
            for found in re.finditer('"(.+)"\\s?|(.+?)?\\b\\s?', cmd_split[1]):
                if found.group(1) is not None:
                    if len(args) < min_args:
                        args.append(found.group(1))
                    else:
                        kwargs.append(found.group(1))
                    continue
                if found.group(2) is not None:
                    if len(args) < min_args:
                        args.append(found.group(2))
                    else:
                        kwargs.append(found.group(2))
                    continue
        if len(args) < min_args:
            raise Exception('Not enough arguments supplied! Expected <code>%i</code> got <code>%i</code>.' % (min_args, len(args)), parse_mode='HTML')
        if len(args) + len(kwargs) > max_args:
            raise Exception('Too many arguments supplied! Expected maximum of <code>%i</code> got <code>%i</code>.' % (max_args, len(args)), parse_mode='HTML')

        real_kwargs = {}
        for i in range(0, len(self.kwargs)):
            kwarg = self.kwargs[i]
            if i < len(kwargs):
                try:
                    real_kwargs[kwarg['name']] = kwarg['type'](kwargs[i])
                except:
                    raise Exception('Invalid argument supplied-- expected <code>%s</code>, got <code>%s</code>.' % (kwarg['type'].__name__, kwargs[i]), parse_mode='HTML')
            else:
                real_kwargs[kwarg['name']] = kwarg['default']
        return (args, real_kwargs)

def cmd(command):
    def inner(func):
        data = get_func_data(func)
        if data.trigger is None: data.trigger = CommandTrigger(command)
        elif not isinstance(data.trigger, CommandTrigger):
            raise Exception('Cannot attach a command trigger to a function with a trigger already specified!')
        else:
            raise Exception('Cannot attach multiple commands to a function with a command specified!')
        return func
    return inner

def arg(name, type=str):
    def inner(func):
        data = get_func_data(func)
        if data.trigger is None:
            raise Exception('Cannot attach an argument to a function with no command specified!')
        elif not isinstance(data.trigger, CommandTrigger):
            raise Exception('Cannot attach a command trigger to a function with a trigger already specified!')
        else:
            raise Exception('Cannot attach multiple commands to a function with a command specified!')

        defaults = get_default_args(func)
        arg = {'name': name, 'type': type}
        if name not in defaults:
            data.trigger.args.append(arg)
        else:
            arg['default'] = defaults[name]
            data.trigger.kwargs.append(arg)
        return func
    return inner
