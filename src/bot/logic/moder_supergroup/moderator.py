"""This file represents an admin logic."""
import time

from aiogram import Router, types, F
from aiogram.filters import Command, or_f

from src.bot.filters.chat_types import IsModerator
from src.bot.kbds.text_builder import MENU_KB
from aiogram.fsm.context import FSMContext
from src.bot.structures.role import Role


moder_router = Router(name='moder')
moder_router.message.filter(IsModerator())


@moder_router.message(Command('moderate'))
async def test(message: types.Message, state: FSMContext, db):
    """Admin command handler."""

    await state.clear()

    try:
        user_id, status = int(message.text.split()[-2]), message.text.split()[-1]
    except IndexError:
        return message.answer('Используйте команду корректно!')

    if status.lower() == '1':
        print("Accepted")
    elif status.lower() == '-1':
        print("Not accepted")
    else:
        return message.answer('Используйте команду корректно!')


@moder_router.message(Command('answer'))
async def answer_question(message: types.Message, state: FSMContext, db, bot):
    """Admin command handler."""

    await state.clear()

    try:
        question_id, answer_text = int(message.text.split()[1]), ' '.join(message.text.split()[2:])
        if not await db.question.is_exists(question_id):
            return message.answer('Вопроса с таким id не существует!')
    except IndexError:
        return message.answer('Используйте команду корректно!')

    await db.question.update_cell(question_id, 'answer_text', answer_text)
    await db.session.commit()

    question = await db.question.get(question_id)

    await bot.send_message(question.user.user_id, answer_text)