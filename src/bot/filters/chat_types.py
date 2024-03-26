from aiogram.filters import Filter
from aiogram import Bot, types
from src.configuration import conf
from src.bot.structures.role import Role


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types
    

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot, db) -> bool:
        if str(message.from_user.id) in conf.admin_list.admin_id:
            return True
        else:
            return False


class IsModerator(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot, role: Role) -> bool:
        if role in [Role.MODERATOR, Role.ADMINISTRATOR] or IsAdmin():
            return True
        else:
            return False
