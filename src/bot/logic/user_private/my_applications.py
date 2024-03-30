
from aiogram import Router, types, F
from aiogram.filters import Command, or_f

from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.kbds.text_builder import MENU_KB
from aiogram.fsm.context import FSMContext


my_applications_router = Router(name='my_applications')
my_applications_router.message.filter(ChatTypeFilter(["private"]))

@my_applications_router.message(F.text.lower() == 'мои заявки')
async def start_handler(message: types.Message, state: FSMContext):
    """Menu command handler."""
    await state.clear()

    await message.answer('Что вас интересует?',
                                reply_markup=MENU_KB
                                )