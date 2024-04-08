
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

moder_to_user_chat_router = Router(name='moder_to_user_chat')
moder_to_user_chat_router.message.filter(IsModerator(), ChatTypeFilter(['supergroup']))


class ModerToUserChat(StatesGroup):
    chat_enter_message_id = State()
    hint_message_id = State()
    messages_id = State()


@moder_to_user_chat_router.message(StateFilter(None), Command('chat'))
async def moder_to_user_chat(message: types.Message, state: FSMContext, bot):

    chat_enter_message = await message.answer(text='✅ | Вы вошли в чат с пользователем.'
                              '\nСледующие сообщения будут пересылаться клиенту при нажатии кнопки <strong>Отправить</strong>',
                         reply_markup=BUTTON_CHAT_EXIT)

    await state.update_data(chat_enter_message_id=chat_enter_message.message_id,
                            messages_id=[])

    await message.delete()

    await state.set_state(ModerToUserChat.messages_id)


@moder_to_user_chat_router.callback_query(StateFilter(ModerToUserChat.messages_id), F.data == 'exit_chat')
async def moder_to_user_chat(callback: types.CallbackQuery, state: FSMContext, bot):

    data = await state.get_data()

    try:
        await bot.delete_message(chat_id=conf.admin.supergroup_id, message_id=data['hint_message_id'])
    except Exception:
        pass

    try:
        await bot.edit_message_text(chat_id=conf.admin.supergroup_id, message_id=data['chat_enter_message_id'],
                                    text='✅ | Вы вошли в чат с пользователем.')
    except Exception:
        pass


    await callback.message.answer(text='❎ | Вы вышли из чата.')

    await state.clear()


@moder_to_user_chat_router.edited_message(StateFilter(ModerToUserChat.messages_id))
@moder_to_user_chat_router.message(StateFilter(ModerToUserChat.messages_id))
async def moder_to_user_chat(message: types.Message, state: FSMContext, bot):

    data = await state.get_data()

    if message.message_id not in data['messages_id']:
        data['messages_id'].append(message.message_id)

    try:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['chat_enter_message_id'],
                                text='✅ | Вы вошли в чат с экспертом.')
    except TelegramBadRequest:
        pass

    await state.update_data(messages_id=data['messages_id'])


    try:

        await bot.delete_message(chat_id=conf.admin.supergroup_id, message_id=data['hint_message_id'])

    except Exception:
        pass

    hint_message = await message.answer(text='❗️ | Вы еще не отправили сообщения', reply_markup=MENU_CHAT)

    await state.update_data(hint_message_id=hint_message.message_id)


@moder_to_user_chat_router.callback_query(StateFilter(ModerToUserChat.messages_id), F.data == 'send_chat')
async def moder_to_user_chat(callback: types.CallbackQuery, state: FSMContext, db, bot):

    data = await state.get_data()

    thread_id = callback.message.message_thread_id
    user_id = await db.user.get_by_thread(thread_id=thread_id)

    print(data['messages_id'])
    for mes_id in data['messages_id']:
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=conf.admin.supergroup_id, message_id=mes_id)
        except TelegramBadRequest:
            pass

    await callback.message.edit_text(text='✏️ | Сообщения отправлены',
                                     reply_markup=BUTTON_CHAT_EXIT)

    await state.update_data(messages_id=[])


@moder_to_user_chat_router.message(Command('test'))
async def moder_to_user_chat(message: types.Message, state: FSMContext, bot):
    await state.clear()