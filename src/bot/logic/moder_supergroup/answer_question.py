"""This file represents an admin logic."""
import time

from aiogram import Router, types, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup

from src.bot.filters.chat_types import IsModerator, ChatTypeFilter
from aiogram.fsm.context import FSMContext

from src.bot.kbds.question_answer_menu_logic import BUTTON_ANSWER_QUESTION, \
    RETURN_QUESTION_MENU
from src.bot.structures.role import Role
from src.configuration import conf
from src.db import Database

answer_question_router = Router(name='answer_question')
answer_question_router.message.filter(IsModerator())

class AnswerQuestion(StatesGroup):
    question_message_id = State()
    hint_message_id = State()
    question_id = State()
    get_answer = State()

@answer_question_router.callback_query(StateFilter(None), F.data.startswith('answer_question_'))
async def acception_acc(callback: types.CallbackQuery, state: FSMContext):


    id = int(callback.data.split('_')[-1])

    await state.update_data(question_id=id)
    await state.update_data(question_message_id=callback.message.message_id)

    await callback.message.delete_reply_markup()


    hint_message = await callback.message.reply(text='Введите ответ на вопрос следующим сообщением и нажмите <strong>Подтвердить</strong>:',
                                  reply_markup=await RETURN_QUESTION_MENU(id))

    await state.update_data(hint_message_id=hint_message.message_id)


    await state.set_state(AnswerQuestion.get_answer)


@answer_question_router.callback_query(AnswerQuestion.get_answer, F.data.startswith('return_'))
async def acception_acc(callback: types.CallbackQuery, state: FSMContext, bot):

    id = int(callback.data.split('_')[-1])

    data = await state.get_data()

    await callback.message.delete()

    try:
        await bot.edit_message_reply_markup(conf.admin.supergroup_id, message_id=data['question_message_id'],
                                            reply_markup=await BUTTON_ANSWER_QUESTION(id))
    except Exception:
        pass

    await state.clear()

@answer_question_router.edited_message(AnswerQuestion.get_answer)
@answer_question_router.message(AnswerQuestion.get_answer)
async def acception_acc(message: types.Message, state: FSMContext, bot):


    await state.update_data(get_answer=message.text)

    data = await state.get_data()

    try:
        await bot.edit_message_text(chat_id= conf.admin.supergroup_id, message_id=data['hint_message_id'],
                                    text='Ваш последний ответ сохранен.'
                                         '\nТекст ответа:'
                                         f'\n<strong>{data["get_answer"]}</strong>'
                                         '\nВы можете отредактировать сообщение',
                                    reply_markup=await RETURN_QUESTION_MENU(data['question_id']))

    except Exception:
        pass




@answer_question_router.callback_query(AnswerQuestion.get_answer, F.data.startswith('send_'))
async def acception_acc(callback: types.CallbackQuery, state: FSMContext, db: Database, bot):

    data = await state.get_data()

    try:

        await db.question.update_answer(data['question_id'], data['get_answer'])
        await db.session.commit()

        question = await db.question.get(data['question_id'])

        await bot.edit_message_text(chat_id=conf.admin.supergroup_id, message_id=data['question_message_id'],
                                    text=f'<strong>📩✅ | Вопрос от пользователя с id <code>{question.user_id}</code></strong>\n\n'
                                    f'<strong>Текст вопроса:</strong>\n{question.question_text}' + '\n\n<strong>✅ На этот вопрос уже дан ответ: </strong>'
                                    f'\n{data["get_answer"]}')

        await bot.delete_message(conf.admin.supergroup_id, message_id=data['hint_message_id'])

        await bot.send_message(chat_id=question.user_id, text=f'📩 | Ответ на ваш вопрос:\n{data["get_answer"]}',
                                reply_to_message_id=question.user_message_id)

        await state.clear()


    except KeyError:

        try:

            await bot.edit_message_text(chat_id=conf.admin.supergroup_id, message_id=data['hint_message_id'],
                                        text='Вы еще не ввели ответ ⛔️',
                                        reply_markup=await RETURN_QUESTION_MENU(data['question_id']))
        except Exception:
            pass

        return








# @moder_router.message(Command('test'))
# async def test(message: types.Message, state: FSMContext, db, bot):
#     """Admin command handler."""
#     await bot.send_document(conf.admin.supergroup_id, document='BQACAgIAAxkBAAI1W2YJ6VDQt4e75j6JBIxsafXSdQ4dAAKnUgACqJ5QSOhT7w5pEBogNAQ',caption='5252', reply_markup=MODERATION_MENU)
#
#
# @moder_router.message(Command('answer'))
# async def answer_question(message: types.Message, state: FSMContext, db, bot):
#     """Admin command handler."""
#
#     await state.clear()
#
#     try:
#         question_id, answer_text = int(message.text.split()[1]), ' '.join(message.text.split()[2:])
#         if not await db.question.is_exists(question_id):
#             return message.answer('Вопроса с таким id не существует!')
#     except IndexError:
#         return message.answer('Используйте команду корректно!')
#
#     await db.question.update_cell(question_id, 'answer_text', answer_text)
#     await db.session.commit()
#
#     question = await db.question.get(question_id)
#
#     await bot.send_message(question.user.user_id, answer_text)