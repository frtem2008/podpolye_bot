from aiogram.filters import BaseFilter
import aiogram.types as t

class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str | list):
        self.chat_type = chat_type

    async def __call__(self, message: t.Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type

