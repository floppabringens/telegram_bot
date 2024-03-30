from aiogram import F, types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.bot.filters.chat_types import ChatTypeFilter

from src.bot.kbds.text_builder import BUTTON_MENU
from src.bot.logic.moder_supergroup.thread_logic import create_thread, answer_thread

question_router = Router(name='question')
question_router.message.filter(ChatTypeFilter(["private"]))


class Question(StatesGroup):
    get_question = State()


# Хендлер для вопроса
@question_router.message(StateFilter(None), F.text.casefold() == 'вопрос')
async def get_quest(message: types.Message, state: FSMContext):
    await message.answer('Введите свой вопрос в чате.',
                         reply_markup=types.ReplyKeyboardRemove()
                         )
    await state.set_state(Question.get_question)


@question_router.message(Question.get_question, F.text)
async def process_quest(message: types.Message, state: FSMContext, db, bot):
    if len(message.text) >= 1000:
        await message.answer(
            'Вопрос не должен превышать 1000 символов. Введите заново или используйте команду /menu для выхода в меню.'
        )
        return
    await state.update_data(get_question=message.text)

    data = await state.get_data()

    user = await db.user.get(message.from_user.id)
    await db.question.new(user=user, question_text=data['get_question'])
    await create_thread(user, db, bot)
    await db.session.commit()

    await state.clear()
    await message.answer('Ваш вопрос обработан. В ближайшее время на него ответит эксперт',
                         reply_markup=BUTTON_MENU
                         )


@question_router.message(Question.get_question)
async def process_quest2(message: types.Message, state: FSMContext):
    await message.answer(
        'Некорректный формат вопроса.'
    )
