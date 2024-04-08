"""This file represents an admin logic."""
import time

from aiogram import Router, types, F
from aiogram.filters import Command, or_f

from src.bot.filters.chat_types import IsAdmin
from aiogram.fsm.context import FSMContext
from src.bot.structures.role import Role


admin_router = Router(name='admin')
admin_router.message.filter(IsAdmin())


@admin_router.message(Command('update_role'))
async def admin_handler(message: types.Message, state: FSMContext, db):
    """Admin command handler."""

    await state.clear()


    try:
        user_id, role = int(message.text.split()[-2]), message.text.split()[-1]
    except IndexError:
        return message.answer('Используйте команду корректно!')

    if role.lower() in ['0', 'user', 'u']:
        role = Role.USER
    elif role.lower() in ['1', 'moder', 'moderator', 'm']:
        role = Role.MODERATOR
    else:
        return message.answer('Используйте команду корректно!')

    if await db.user.is_exists(user_id):
        await db.user.update_role(user_id, role)
        await db.session.commit()
        await message.answer(f'Роль {role.name} была выдана пользователю {user_id}.')
    else:
        await message.answer(f'Пользователя с id {user_id} нет в таблице.')

