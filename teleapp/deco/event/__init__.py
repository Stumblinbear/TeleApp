import telepot

from ...registry import get_func_data, Trigger


class EventTrigger(Trigger):
    def __init__(self):
        self.events = []

    def test(self, msg):
        return True

    def fire(self, msg):
        for event in self.events:
            if event(msg):
                return True
        return False

def add_event(lamb):
    def inner(func):
        data = get_func_data(func)
        if data.trigger is None: data.trigger = EventTrigger()
        elif not isinstance(data.trigger, EventTrigger):
            raise Exception('Cannot attach an event trigger to a function with a trigger already specified!')

        data.trigger.events.append(lamb)

        return func
    return inner

def content_type(content_type):
    if content_type not in telepot.all_content_types:
        raise Exception('Content type must be one of the following: %r' % ', '.join(telepot.all_content_types))
    return add_event(lambda msg: msg.content_type == content_type)

def edited_message(func):
    return add_event(lambda msg: 'edit_date' in msg.raw)(func)

# Create an event decorator for each content type
import sys
mod = sys.modules[__name__]
for ctype in telepot.all_content_types:
    setattr(mod, ctype, lambda: content_type(ctype))

#text, audio, document, game, photo, sticker, video, voice, video_note, contact, location, venue, new_chat_member, left_chat_member, new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created, channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message, new_chat_members, invoice, successful_payment
