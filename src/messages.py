import json
import re

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.middleware.UserHandlers import bot_logger

messages = {}
chanced_messages = {}


def edit_kwags(j: dict, kwargs: dict):
    for item in j.items():
        kwargs[item[0]] = item[1]


# TODO: Add reply option for normal messages too
def format_normal(name: str, **kwargs):
    edit_kwags(messages, kwargs)
    return messages[name].format(**kwargs)


def format_chanced(name: str, **kwargs):
    edit_kwags(chanced_messages[name], kwargs)
    kwargs['chance_percent'] = chanced_messages[name]['chance'] * 100
    reply = chanced_messages[name]['reply'] if 'reply' in chanced_messages[name] else None
    return chanced_messages[name]['chance'], chanced_messages[name]['text'].format(**kwargs), reply


def is_conditional(name):
    return "triggers" in chanced_messages[name]


def triggers(name: str):
    return chanced_messages[name]['triggers']


def chancedNames():
    return [m for m in chanced_messages.keys()]


# TODO add picture, sticker, audio, etc triggers
def process_triggers(params: dict):
    if 'triggers' in params:
        if 'text matches' in params['triggers']:
            params['triggers']['regex'] = re.compile(params['triggers']['text matches'])


def reload(name: str):
    global messages, chanced_messages

    with open(f'./res/{name}.json') as f:
        messages = json.load(f)
        chanced_messages = messages["chanced"]
        for name, params in chanced_messages.items():
            bot_logger.info(f'Message name: {name}; send params: {params}')
            process_triggers(params)

        chanced_messages[name] = params

    bot_logger.info(messages)
    bot_logger.info(chanced_messages)

    bot_logger.info('Messages reloaded')


class MessagesUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == 'res/messages.json':
            bot_logger.info(event)
            reload('messages')


if not messages:
    reload('messages')

    observer = Observer()
    event_handler = MessagesUpdateHandler()

    directory_to_watch = "res"
    observer.schedule(event_handler, directory_to_watch, recursive=True)
    observer.start()
