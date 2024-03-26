from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.bot.filters.chat_types import ChatTypeFilter

from src.bot.kbds.text_builder import BUTTON_CONTINUE, BUTTON_AGREE

flood_exp_router = Router()
flood_exp_router.message.filter(ChatTypeFilter(["private"]))

class FloodExp(StatesGroup):
    get_flood = State()
    give_agreement = State()
    continue_flood = State()
    application_on_flood = State()


# Хендлер для экспертизы
@flood_exp_router.message(State(None), F.text.casefold() == 'экспертиза по затоплению')
async def get_flood(message: types.Message, state: FSMContext):
    await message.answer('Инструкция',
                         reply_markup=BUTTON_CONTINUE
                         )
    await state.set_state(FloodExp.continue_flood)



@flood_exp_router.message(FloodExp.continue_flood, F.text.casefold() == 'продолжить')
async def get_flood1(message: types.Message, state: FSMContext):
    await message.answer('Необходимо соглашение на сбор персональных данных.',
                         reply_markup=BUTTON_AGREE
                         )
    await state.set_state(FloodExp.give_agreement)


@flood_exp_router.message(FloodExp.give_agreement, F.text.casefold() == 'не имею ничего против')
async def get_flood1(message: types.Message, state: FSMContext):
    await message.answer('Для проведения эĸспертизы нам нужно уточнить несĸольĸо деталей.',
                         reply_markup=BUTTON_CONTINUE
                         )
    await state.set_state(FloodExp.application_on_flood)





