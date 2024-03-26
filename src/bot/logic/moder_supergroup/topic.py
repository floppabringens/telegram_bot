
"""This file represents an admin logic."""

from aiogram import Router, types, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.methods.create_forum_topic import CreateForumTopic
from aiogram.methods import create_forum_topic, delete_forum_topic


from src.bot.filters.chat_types import IsModerator

from src.bot.filters.chat_types import ChatTypeFilter

supergroup_router = Router(name='supergroup')
supergroup_router.message.filter(IsModerator(), ChatTypeFilter(['supergroup']))


@supergroup_router.message(Command('create_topic'))
async def test(message: types.Message, state: FSMContext, bot):
    create_topic = CreateForumTopic(
        chat_id='-1002118512136',
        name='Stepa daun'
    )

    # await bot.create_forum_topic(create_topic)

    ForumTopic = await bot.create_forum_topic(chat_id='-1002118512136', name='Stepa daun')

    await message.answer(str(ForumTopic))

 