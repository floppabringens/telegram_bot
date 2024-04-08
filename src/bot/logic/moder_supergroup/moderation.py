"""This file represents an admin logic."""
import time

from aiogram import Router, types, F
from aiogram.filters import Command, or_f
from aiogram.types import ForceReply

from src.bot.filters.chat_types import IsModerator, ChatTypeFilter
from src.bot.kbds.app_moderation_menu_logic import CONFIRMATION_DEC_MENU, CONFIRMATION_ACC_MENU, MODERATION_MENU
from aiogram.fsm.context import FSMContext

from src.bot.kbds.text_builder import MENU_NO_APPS_KB
from src.bot.structures.role import Role
from src.bot.logic.moder_supergroup.thread_work import send_all_flood_apps
from src.configuration import conf
from src.db import Database

moder_router = Router(name='moder')
moder_router.message.filter(IsModerator())

@moder_router.callback_query(F.data.startswith('accept_'))
async def acception_acc(callback: types.CallbackQuery, db: Database):
    await callback.answer('Вы уверены?')
    id = int(callback.data.split('_')[-1])
    await callback.message.edit_reply_markup(reply_markup=await CONFIRMATION_ACC_MENU(id))

@moder_router.callback_query(F.data.startswith('decline_'))
async def acception_dec(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Вы уверены?')
    id = int(callback.data.split('_')[-1])
    await callback.message.edit_reply_markup(reply_markup=await CONFIRMATION_DEC_MENU(id))


@moder_router.callback_query(F.data.startswith('acc_confirm_'))
async def acception_acc(callback: types.CallbackQuery, db):
    await callback.answer('Заявка принята')

    id = int(callback.data.split('_')[-1])
    await db.flood_application.update_status(id, 1)
    await db.session.commit()

    await callback.message.edit_caption(caption=f'<strong>Заявка <code>{id}</code> принята</strong>')

@moder_router.callback_query(F.data.startswith('dec_confirm_'))
async def acception_acc(callback: types.CallbackQuery, db):
    await callback.answer('Заявка отклонена')

    id = int(callback.data.split('_')[-1])
    await db.flood_application.update_status(id, 2)
    await db.session.commit()

    await callback.message.edit_caption(caption=f'<strong>Заявка <code>{id}</code> отклонена</strong>')

@moder_router.callback_query(F.data.startswith('return_'))
async def acception_acc(callback: types.CallbackQuery, db: Database):
    id = int(callback.data.split('_')[-1])
    await callback.message.edit_reply_markup(reply_markup=await MODERATION_MENU(id))



@moder_router.message(Command('all'))
async def test(message: types.Message, state: FSMContext, db, bot):
    """Admin command handler."""

    await state.clear()

    try:
        user_id, status = int(message.text.split()[-2]), message.text.split()[-1]
    except IndexError:
        return message.answer('Используйте команду корректно!')
    user = db.user.get(user_id)
    await send_all_flood_apps(user, bot)

@moder_router.message(Command('test'))
async def test(message: types.Message, state: FSMContext, db, bot):
    """Admin command handler."""
    await message.reply(
                            text = 'wegwgw',
                            reply_markup=ForceReply(force_reply=True, selective=True))


