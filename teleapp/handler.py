import traceback
import re
import time
import asyncio

import telepot

from . import botan
from . import registry


class UpdateWrapper:
    def __init__(self, handler, raw):
        self.bot = handler.bot
        self.sender = handler.sender

        self.flavor = telepot.flavor(raw)

        if self.flavor == 'inline_query':
            self.query_id, self.from_id, self.query_string = telepot.glance(raw, flavor=self.flavor)
            self.answerer = handler.answerer
        elif self.flavor == 'chosen_inline_query':
            self.result_id, self.from_id, self.query_string = telepot.glance(raw, flavor=self.flavor)
        else:
            self.content_type, self.chat_type, self.chat_id = telepot.glance(raw)

        self.raw = raw

    @property
    def message(self):
        return self.raw

    @property
    def id(self):
        if self.flavor == 'chat': return self.raw['message_id']
        if self.flavor == 'result_id': return self.raw['result_id']
        return self.raw['id']

    @property
    def text(self):
        if 'text' in self.raw: return self.raw['text']
        if 'query' in self.raw: return self.raw['query']
        return None

    @property
    def file_id(self):
        if 'document' in self.raw: return self.raw['document']['file_id']
        return None

    def glance(self):
        return telepot.glance(self.raw, flavor=self.flavor)

    def content(self):
        return telepot.peel(self.raw)

    def answer(self, answer):
        self.answerer.answer(self.raw, answer)

class TeleChat(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TeleChat, self).__init__(*args, **kwargs)

    async def on_chat_message(self, message):
        await handle_message_thing(self, message, 'Message')

class TeleInline(telepot.aio.helper.InlineUserHandler, telepot.aio.helper.AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(TeleInline, self).__init__(*args, **kwargs)

    async def on_inline_query(self, message):
        await handle_message_thing(self, message, 'Inline')

    async def on_chosen_inline_result(self, message):
        await handle_message_thing(self, message, None)

async def handle_message_thing(handler, message, event_name):
    # Don't reply to messages outside the reply threshold
    if handler.bot.reply_threshold > -1:
        if 'date' in message:
            date = message['date'] if not 'edit_date' in message else message['edit_date']
            if date + handler.bot.reply_threshold < int(time.time()):
                return

    update = UpdateWrapper(handler, message)

    triggered = False
    for func, data in registry.get_registered().items():
        if data.test(update):
            success = await data.fire(update)
            if success:
                triggered = True
    if event_name is not None and triggered:
        botan.track(message['from']['id'], message, event_name)
    else:
        botan.track(message['from']['id'], message, 'Ignored')

