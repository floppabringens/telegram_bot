
"""This file represents an admin logic."""

from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from src.bot.filters.chat_types import IsModerator

from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.kbds.text_builder import BUTTON_CHAT_EXIT, MENU_CHAT
from src.configuration import conf

user_to_moder_chat_router = Router(name='user_to_moder_chat')
user_to_moder_chat_router.message.filter(ChatTypeFilter(['private']))


class UserToModerChat(StatesGroup):
    chat_enter_message_id = State()
    hint_message_id = State()
    messages_id = State()


@user_to_moder_chat_router.message(StateFilter(None), F.text.casefold() == ('чат с экспертом'))
async def user_to_moder_chat(message: types.Message, state: FSMContext, bot):

    chat_enter_message = await message.answer(text='✅ | Вы вошли в чат с экспертом.'
                              '\nСледующие сообщения будут пересылаться эксперту при нажатии кнопки <strong>Отправить</strong>',
                         reply_markup=BUTTON_CHAT_EXIT)

    await state.update_data(chat_enter_message_id=chat_enter_message.message_id,
                            messages_id=[])

    await state.set_state(UserToModerChat.messages_id)


@user_to_moder_chat_router.callback_query(StateFilter(UserToModerChat.messages_id), F.data == 'exit_chat')
async def user_to_moder_chat(callback: types.CallbackQuery, state: FSMContext, bot):

    data = await state.get_data()

    try:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['hint_message_id'])
    except KeyError:
        pass

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id, message_id=data['chat_enter_message_id'],
                                text='✅ | Вы вошли в чат с экспертом.')
    except TelegramBadRequest:
        pass


    await callback.message.answer(text='❎ | Вы вышли из чата.')

    await state.clear()


@user_to_moder_chat_router.edited_message(StateFilter(UserToModerChat.messages_id))
@user_to_moder_chat_router.message(StateFilter(UserToModerChat.messages_id))
async def user_to_moder_chat(message: types.Message, state: FSMContext, bot):

    data = await state.get_data()

    try:
        if message.message_id > data['messages_id'][-1]:
            data['messages_id'].append(message.message_id)
        else:
            for step, mes_id in enumerate(data['messages_id']):
                if mes_id == message.message_id:
                    data['messages_id'][step] = message.message_id
    except IndexError:
        data['messages_id'].append(message.message_id)

    try:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['chat_enter_message_id'],
                                text='✅ | Вы вошли в чат с экспертом.')
    except TelegramBadRequest:
        pass

    await state.update_data(messages_id=data['messages_id'])


    try:

        await bot.delete_message(chat_id=message.from_user.id, message_id=data['hint_message_id'])

    except Exception:
        pass

    hint_message = await message.answer(text='❗️ | Вы еще не отправили сообщения', reply_markup=MENU_CHAT)

    await state.update_data(hint_message_id=hint_message.message_id)

@user_to_moder_chat_router.callback_query(StateFilter(UserToModerChat.messages_id), F.data == 'send_chat')
async def user_to_moder_chat(callback: types.CallbackQuery, state: FSMContext, db, bot):

    data = await state.get_data()

    user_id = callback.from_user.id
    user = await db.user.get(ident=user_id)
    thread_id = user.thread_id

    for mes_id in data['messages_id']:
        try:
            await bot.forward_message(chat_id=conf.admin.supergroup_id, from_chat_id=callback.from_user.id,
                                   message_thread_id=thread_id, message_id=mes_id)
        except Exception:
            pass

    await callback.message.edit_text(text='✏️ | Сообщения отправлены',
                                     reply_markup=BUTTON_CHAT_EXIT)

    await state.update_data(messages_id=[])