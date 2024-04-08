"""This file represents a start logic."""

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.kbds.main_menu_logic import MENU_KB
from src.configuration import conf


start_router = Router(name='start')
start_router.message.filter(ChatTypeFilter(["private"]))


@start_router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext, db):
    """Start command handler."""
    await state.clear()

    if not await db.user.is_exists(message.from_user.id):
        await db.user.new(user_id=message.from_user.id)
        await db.session.commit()

    user = await db.user.get(message.from_user.id)


    await message.answer('Здравствуйте. Этот бот поможет вам заполнить заявку по необходимой экспертизе.',
                                reply_markup=await MENU_KB(user)
                                )
