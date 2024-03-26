"""This file represent startup bot logic."""
import asyncio
import logging

from aiogram import Bot, types
from redis.asyncio.client import Redis

from src.bot.dispatcher import get_dispatcher, get_redis_storage
from src.bot.structures.data_structure import TransferData
from src.configuration import conf
from src.db.database import create_async_engine
from  src.bot.structures.role import Role


from common.bot_cmds_list import private


async def on_startup(bot):
    pass


async def on_shutdown(bot):
    print('бот лег')


async def start_bot():
    """This function will start bot with polling mode."""
    bot = Bot(token=conf.bot.token)
    storage = get_redis_storage(
        redis=Redis(
            db=conf.redis.db,
            host=conf.redis.host,
            password=conf.redis.passwd,
            username=conf.redis.username,
            port=conf.redis.port,
        )
    )
    dp = get_dispatcher(storage=storage)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(engine=create_async_engine(url=conf.db.build_connection_str())
                       )
        )


if __name__ == '__main__':
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(
        start_bot())
