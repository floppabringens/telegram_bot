"""This file represents a menu logic."""
import time

from aiogram import Router, types, F
from aiogram.filters import Command, or_f

from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.kbds.text_builder import MENU_KB
from aiogram.fsm.context import FSMContext


menu_router = Router(name='menu')
menu_router.message.filter(ChatTypeFilter(["private"]))

@menu_router.message(or_f(Command('menu'), F.text.casefold() == 'menu', F.text.casefold() == 'меню'))
async def start_handler(message: types.Message, state: FSMContext):
    """Menu command handler."""
    await state.clear()
    await message.answer('Что вас интересует?',
                                reply_markup=MENU_KB
                                )

# @menu_router.message(F.document)
# async def add_image(message: types.Message, state: FSMContext):
#     data = message.document.file_id
#     await message.answer("Товар добавлен")
#     await message.answer_document(data)
#     print(data)