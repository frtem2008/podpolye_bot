import json
import re

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.logs import logsetup

message_dict = {}
random_messages = {}

log = logsetup.new_logger('Message loader')


# TODO: Add reply option for normal messages too
def format_normal(name: str, **kwargs) -> str:
    kwargs.update(message_dict)
    return message_dict[name].format(**kwargs)


def format_random(name: str, **kwargs) -> tuple[float, str, bool]:
    kwargs.update(random_messages[name])
    kwargs['chance_percent'] = random_messages[name]['chance'] * 100
    reply = random_messages[name]['reply'] if 'reply' in random_messages[name] else None
    return random_messages[name]['chance'], random_messages[name]['text'].format(**kwargs), reply


def has_triggers(name) -> bool:
    return "triggers" in random_messages[name]


def triggers(name: str) -> dict[str, str]:
    return random_messages[name]['triggers']


def random_messages_names() -> list[str]:
    return [m for m in random_messages.keys()]


# TODO: add picture, sticker, audio, etc triggers
def process_triggers(params: dict) -> None:
    if 'triggers' in params:
        if 'text matches' in params['triggers']:
            # TODO: add regex compilation parameters (f.e. ignorecase)
            params['triggers']['regex'] = re.compile(params['triggers']['text matches'])


def text_separator() -> str:
    return message_dict["text separator"]


def rofl_triggers() -> dict[str, str]:
    return message_dict["rofl triggers"]


def reload() -> None:
    global message_dict, random_messages

    with open(f'res/messages.json') as f:
        message_dict = json.load(f)
        random_messages = message_dict["random"]
        for name, params in random_messages.items():
            log.debug(f'Message name: {name}; send params: {params}')
            process_triggers(params)

        random_messages[name] = params

    log.debug(message_dict)
    log.debug(random_messages)

    log.info('Messages reloaded')


class MessagesUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event) -> None:
        if event.src_path == 'res/messages.json':
            log.debug(f'Filesystem event handler: {event}')
            reload()


if not message_dict:
    reload()

    observer = Observer()
    event_handler = MessagesUpdateHandler()

    directory_to_watch = "res"
    observer.schedule(event_handler, directory_to_watch, recursive=True)
    observer.start()
