import asyncio
import time

import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, per_inline_from_id, create_open, pave_event_space

from . import botan
from .handler import TeleChat, TeleInline


class TeleApp(telepot.aio.DelegatorBot):
    def __init__(self, token, reply_threshold=60, botan_key=None):
        super(TeleApp, self).__init__(token, [
            pave_event_space()(
                    per_chat_id(), create_open,
                    TeleChat, timeout=10
                ),
            pave_event_space()(
                    per_inline_from_id(), create_open,
                    TeleInline, timeout=10
                )
        ])

        self.reply_threshold = reply_threshold

        botan.set_key(botan_key)

        self._loop = asyncio.get_event_loop() 

        self.username = self._loop.run_until_complete(self.getMe())['username']

    def start(self, forever=True):
        self._loop.create_task(MessageLoop(self).run_forever())

        print('Listening ...')
        self._loop.run_forever()
