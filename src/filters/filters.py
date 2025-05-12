import telebot.types
from telebot.custom_filters import SimpleCustomFilter


class OneArgumentFilter(SimpleCustomFilter):
    key = 'oneargument'

    def check(self, message: telebot.types.Message) -> bool:
        return len(telebot.util.extract_arguments(message.text).strip().split()) == 1


class TwoArgumentsFilter(SimpleCustomFilter):
    key = 'twoarguments'

    def check(self, message: telebot.types.Message) -> bool:
        return len(telebot.util.extract_arguments(message.text).strip().split()) == 2
