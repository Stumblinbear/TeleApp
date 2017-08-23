import asyncio
import time

import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

from .handler import TeleChat


class TeleApp(telepot.DelegatorBot):
    def __init__(self, token, reply_threshold=60):
        super(TeleApp, self).__init__(token, [
            pave_event_space()(
                    per_chat_id(), create_open,
                    TeleChat, timeout=10
                ),
        ])

        self.reply_threshold = reply_threshold

        self.username = self.getMe()['username']

    def start(self, forever=True):
        MessageLoop(self).run_as_thread()

        if forever:
            while True:
                time.sleep(1)
