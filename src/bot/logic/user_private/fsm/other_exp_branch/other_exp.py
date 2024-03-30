from aiogram import F, types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.bot.filters.chat_types import ChatTypeFilter

from src.bot.kbds.text_builder import BUTTON_MENU
from src.bot.logic.moder_supergroup.thread_logic import create_thread

other_exp_router = Router()
other_exp_router.message.filter(ChatTypeFilter(["private"]))


class OtherExp(StatesGroup):
    get_expertise = State()


# Хендлер для экспертизы
@other_exp_router.message(StateFilter(None), F.text.casefold() == 'экспертиза другого вида')
async def get_exp(message: types.Message, state: FSMContext):
    await message.answer('Какая экспертиза вам необходима?',
                         reply_markup=types.ReplyKeyboardRemove()
                         )
    await state.set_state(OtherExp.get_expertise)


@other_exp_router.message(OtherExp.get_expertise, F.text)
async def process_exp(message: types.Message, state: FSMContext, db, bot):
    if len(message.text) >= 1000:
        await message.answer(
            'Описание экспертизы не должно превышать 1000 символов. Введите заново или используйте команду /menu для выхода в меню.'
        )
        return
    await state.update_data(get_expertise=message.text)
    await state.update_data(get_question=message.text)

    data = await state.get_data()

    user = await db.user.get(message.from_user.id)
    await db.question.new(user=user, question_text=data['get_question'])
    await create_thread(user, db, bot)
    await db.session.commit()

    await state.clear()
    await message.answer('Ваш вопрос обработан. В ближайшее время с вами свяжется эксперт для проведения консультации.',
                         reply_markup=BUTTON_MENU
                         )


@other_exp_router.message(OtherExp.get_expertise)
async def process_exp2(message: types.Message, state: FSMContext):
    await message.answer(
        'Некорректный формат вопроса.'
    )
