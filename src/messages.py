import json

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.middleware.UserHandlers import bot_logger

messages = {}
chanced_messages = {}


def edit_kwags(j: dict, kwargs: dict):
    for item in j.items():
        kwargs[item[0]] = item[1]


def msg(name: str, **kwargs):
    edit_kwags(messages, kwargs)
    return messages[name].format(**kwargs)


def chanced(name: str, **kwargs):
    edit_kwags(chanced_messages[name], kwargs)
    kwargs['chance_percent'] = chanced_messages[name]['chance'] * 100
    return chanced_messages[name]['chance'], chanced_messages[name]['text'].format(**kwargs)


def is_conditional(name):
    return "triggered by" in chanced_messages[name]


def chancedNames():
    return [m[0] for m in chanced_messages.items()]


def reload(name: str):
    global messages, chanced_messages

    with open(f'./res/{name}.json') as f:
        messages = json.load(f)
        chanced_messages = messages["chanced"]
        for m in chanced_messages.items():
            chanced_messages[m[0]] = m[1]

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
