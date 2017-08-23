TeleApp
=======
-------

***Warning: The detector does not stop once an event or command was successfully matched. All of them are checked, and all of them are ran if able.***

Setup:
------
```
from teleapp import TeleApp

# Reply threshold is the maximum amount of seconds in the past
# that the bot should respond to. This prevents a mass of
# messages from being posted if the bot was offline for a time
# set this to -1 if you don't want a threshold.
app = TeleApp(token=BOT_TOKEN, reply_threshold=10)

# Triggers here

app.start()
```

Commands:
---------
```
from teleapp.deco.cmd import cmd, arg

# Listen to /start
@cmd('start')
def start_bot(update):
    update.sender.sendMessage('Started!')

# Listen for /echo and reply with the message sent x times
# Echo message must be wrapped in quotes
# Arguments with no default value set in the function parameters
# are required. If a default value is set, the argument is optional.
# /echo "testing message"
#        bot responds with "testing message" one time
# /echo "testing message" 4
#        bot responds with "testing message" four times
@cmd('echo')
@arg('text')
@arg('times', type=int)
def bot_echo(update, text, times=1):
    for i in range(0, times):
      update.sender.sendMessage(text)
```

Triggers:
---------
```
from teleapp.deco.text import contains, equals, regex

# Respond to messages containing "chill"
@contains('chill')
# Also responds to messages that are exactly equal to "wo chill"
@equals('wo chil', sensitive=True)
# Also respons to messages that start with 🅱️
@regex('^🅱️')
def respond_chill(update):
    update.sender.sendMessage('no u')
```

Events:
-------
*List of events can be aquired by outputting `telepot.all_content_types`*
```
import teleapp.deco.event as event

# Respond when a message with only text was received
@event.content_type('text')
def on_text_message(update):
    update.sender.sendMessage('Received message with text')

# Respond when a message with only text was received
@event.text
def on_text_message(update):
    update.sender.sendMessage('Received message with text')

# Respond when any message was edited
@event.edit_message
def on_edit_message(update):
    update.sender.sendMessage('message was edited!')
```
