import re
import time

import telepot

from . import registry


class MessageWrapper:
    def __init__(self, handler, raw):
        self.bot = handler.bot
        self.sender = handler.sender

        self.flavor = telepot.flavor(raw)

        self.content_type, self.chat_type, self.chat_id = telepot.glance(raw)
        self.raw = raw

    @property
    def id(self):
        if self.flavor == 'chat': return self.raw['message_id']
        if self.flavor == 'result_id': return self.raw['result_id']
        return self.raw['id']

    @property
    def text(self):
        return self.raw['text'] if 'text' in self.raw else None

    def glance(self):
        return telepot.glance(self.raw, flavor=self.flavor)

    def content(self):
        return telepot.peel(self.raw)

class TeleChat(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TeleChat, self).__init__(*args, **kwargs)

    def on_chat_message(self, message):
        # Don't reply to messages outside the reply threshold
        date = message['date'] if not 'edit_date' in message else message['edit_date']
        if date + self.bot.reply_threshold < int(time.time()):
            return

        msg = MessageWrapper(self, message)

        for func, data in registry.get_registered().items():
            if data.test(msg):
                if data.fire(msg):
                    break
