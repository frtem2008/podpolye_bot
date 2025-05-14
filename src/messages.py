import json

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.middleware.UserHandlers import bot_logger

messages = {}


def msg(name: str, **kwargs):
    return messages[name].format(**kwargs)


def reload(name: str):
    global messages

    with open(f'./res/{name}.json') as f:
        messages = json.load(f)
        bot_logger.info(messages)

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
