from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.bot.filters.chat_types import ChatTypeFilter

from src.bot.kbds.text_builder import BUTTON_CONTINUE, BUTTON_AGREE

flood_exp_router = Router()
flood_exp_router.message.filter(ChatTypeFilter(["private"]))

class FloodExp(StatesGroup):
    application_on_flood = State()


# Хендлер для экспертизы
@flood_exp_router.message(State(None), F.text.casefold() == 'экспертиза по затоплению')
async def get_flood(message: types.Message, state: FSMContext):
    await message.answer('Инструкция',
                         reply_markup=BUTTON_CONTINUE
                         )
    await state.set_state(FloodExp.application_on_flood)







